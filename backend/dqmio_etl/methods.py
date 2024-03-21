import logging
import os
import shutil
import tempfile

from django.conf import settings
from dqmio_file_indexer.models import FileIndex, FileIndexStatus

from .models import Lumisection, LumisectionHistogram1D, LumisectionHistogram2D, Run
from .reader import DQMIOReader


logger = logging.getLogger(__name__)


class HistIngestion:
    H1D_VALID_MES = (3, 4, 5)
    H2D_VALID_MES = (6, 7, 8)

    def __init__(self, file_index_id: int) -> None:
        self.file_index = FileIndex.objects.get(id=file_index_id)
        self.remote_fpath = self.file_index.file_path

        # Copy remote file to tmp location
        self._tmp_dir = tempfile.mkdtemp()
        self._saved_umask = os.umask(0o077)
        self._fname = "dqmio_ingestion_copy.root"
        self.tmp_fpath = os.path.join(self._tmp_dir, self._fname)
        shutil.copy(self.remote_fpath, self.tmp_fpath)

        # Open reader using tmp location
        self.reader = DQMIOReader(self.tmp_fpath)

    def __ingest_runs_and_lumis(self):
        track_created_runs = {}
        index = []

        for run, lumi in self.reader.list_lumis():
            if run not in track_created_runs:
                run_obj, _ = Run.objects.get_or_create(run_number=run)
                track_created_runs[run] = run_obj

            run_obj = track_created_runs[run]
            lumi_obj, _ = Lumisection.objects.get_or_create(run=run_obj, ls_number=lumi)
            index.append({"run_number": run, "lumi_number": lumi, "lumi_obj": lumi_obj})

        return index

    def __get_h1d_entries_from_root_me(self, me, lumi_obj):
        me_name = me.name
        entries = me.data.GetEntries()
        hist_x_bins = me.data.GetNbinsX()
        hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
        hist_x_max = me.data.GetXaxis().GetBinLowEdge(hist_x_bins + 1)  # Takes low edge of overflow bin instead.
        data = [me.data.GetBinContent(i) for i in range(1, hist_x_bins + 1)]
        return LumisectionHistogram1D(
            lumisection=lumi_obj,
            title=me_name,
            entries=entries,
            data=data,
            source_data_file=self.file_index,
            x_min=hist_x_min,
            x_max=hist_x_max,
            x_bin=hist_x_bins,
        )

    def __get_h2d_entries_from_root_me(self, me, lumi_obj):
        me_name = me.name
        entries = me.data.GetEntries()
        hist_x_bins = me.data.GetNbinsX()
        hist_y_bins = me.data.GetNbinsY()
        hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
        hist_x_max = me.data.GetXaxis().GetBinLowEdge(hist_x_bins) + me.data.GetXaxis().GetBinWidth(hist_x_bins)
        hist_y_min = me.data.GetYaxis().GetBinLowEdge(1)
        hist_y_max = me.data.GetYaxis().GetBinLowEdge(hist_y_bins) + me.data.GetYaxis().GetBinWidth(hist_y_bins)

        # data should be in the form of data[x][y]
        data = [[me.data.GetBinContent(j, i) for j in range(1, hist_x_bins + 1)] for i in range(1, hist_y_bins + 1)]

        return LumisectionHistogram2D(
            lumisection=lumi_obj,
            title=me_name,
            entries=entries,
            data=data,
            source_data_file=self.file_index,
            x_min=hist_x_min,
            x_max=hist_x_max,
            x_bin=hist_x_bins,
            y_min=hist_y_min,
            y_max=hist_y_max,
            y_bin=hist_y_bins,
        )

    def etl(self, obj_index: dict) -> int:
        if self.file_index.n_entries == 0:
            self.file_index.update_entries(
                "n_entries", self.reader.count_mes(whitelist_mes=settings.DQMIO_MES_TO_INGEST)
            )

        h1d_entries_ingested = 0
        h2d_entries_ingested = 0

        for objs in obj_index:
            run_number = objs["run_number"]
            lumi_number = objs["lumi_number"]
            lumi_obj = objs["lumi_obj"]
            me_list = self.reader.get_mes_for_lumi(run_number, lumi_number, "*")
            h1d_list = []
            h2d_list = []
            for me in me_list:
                if me.name not in settings.DQMIO_MES_TO_INGEST:
                    continue
                if me.type in self.H1D_VALID_MES:
                    h1d_list.append(self.__get_h1d_entries_from_root_me(me, lumi_obj))
                elif me.type in self.H2D_VALID_MES:
                    h2d_list.append(self.__get_h2d_entries_from_root_me(me, lumi_obj))

            n_ingested_h1d = len(LumisectionHistogram1D.objects.bulk_create(h1d_list, ignore_conflicts=True))
            n_ingested_h2d = len(LumisectionHistogram2D.objects.bulk_create(h2d_list, ignore_conflicts=True))
            h1d_entries_ingested += n_ingested_h1d
            h2d_entries_ingested += n_ingested_h2d

            # Update n_entries_ingested in FileIndex each run/lumi to keep track of progress
            self.file_index.n_entries_ingested += n_ingested_h1d + n_ingested_h2d
            self.file_index.save()

        # Close files after ingesting and delete tmp file
        self.reader.close()
        os.remove(self.tmp_fpath)
        os.umask(self._saved_umask)
        os.rmdir(self._tmp_dir)

        return h1d_entries_ingested, h2d_entries_ingested

    def run(self):
        """
        Ingest both H1D and H2D
        """
        try:
            self.file_index.update_status(FileIndexStatus.RUNNING)
            obj_index = self.__ingest_runs_and_lumis()
            h1d_entries_ingested, h2d_entries_ingested = self.etl(obj_index)
            self.file_index.update_status(FileIndexStatus.PROCESSED)
        except Exception as err:
            os.remove(self.tmp_fpath)
            os.umask(self._saved_umask)
            os.rmdir(self._tmp_dir)
            self.file_index.update_status(FileIndexStatus.FAILED)
            raise err

        return {
            "h1d_entries": h1d_entries_ingested,
            "h2d_entries": h2d_entries_ingested,
        }
