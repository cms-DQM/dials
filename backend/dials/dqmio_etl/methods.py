import logging

from dqmio_file_indexer.models import FileIndex, FileIndexStatus

from .models import Lumisection, LumisectionHistogram1D, LumisectionHistogram2D, Run
from .reader import DQMIOReader

logger = logging.getLogger(__name__)


class HistIngestion:
    H1D_VALID_MES = (3, 4, 5)
    H2D_VALID_MES = (6, 7, 8)

    def __init__(self, file_index_id: int) -> None:
        self.file_index = FileIndex.objects.get(id=file_index_id)
        self.reader = DQMIOReader(self.file_index.file_path)
        if self.file_index.n_entries == 0:
            self.file_index.update_entries("n_entries", self.reader.count_mes())

    def __h1d(self) -> int:
        entries_ingested = 0

        for run, lumi in self.reader.list_lumis():
            h1d_list = []
            me_list = self.reader.get_mes_for_lumi(run, lumi, "*")

            for me in me_list:
                if me.type not in self.H1D_VALID_MES:
                    continue

                entries = me.data.GetEntries()
                hist_x_bins = me.data.GetNbinsX()
                hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
                hist_x_max = me.data.GetXaxis().GetBinLowEdge(
                    hist_x_bins + 1
                )  # Takes low edge of overflow bin instead.
                data = [me.data.GetBinContent(i) for i in range(1, hist_x_bins + 1)]

                run_obj, _ = Run.objects.get_or_create(run_number=me.run)
                lumi_obj, _ = Lumisection.objects.get_or_create(run=run_obj, ls_number=me.lumi)

                count_lumih1d = LumisectionHistogram1D.objects.filter(lumisection=lumi_obj, title=me.name).count()
                if count_lumih1d == 0:
                    h1d_list.append(
                        LumisectionHistogram1D(
                            lumisection=lumi_obj,
                            title=me.name,
                            entries=entries,
                            data=data,
                            source_data_file=self.file_index,
                            x_min=hist_x_min,
                            x_max=hist_x_max,
                            x_bin=hist_x_bins,
                        )
                    )

            n_ingested = len(LumisectionHistogram1D.objects.bulk_create(h1d_list, ignore_conflicts=True))
            entries_ingested += n_ingested
            logger.debug(
                f"{n_ingested} x 1D lumisection histos successfully added from file {self.file_index.file_path}."
            )

            self.file_index.n_entries_ingested += n_ingested
            self.file_index.save()

        return entries_ingested

    def __h2d(self, read_chunk_lumi: int = -1) -> int:
        entries_ingested = 0
        current_lumi = 0

        for run, lumi in self.reader.list_lumis():
            h2d_list = []
            me_list = self.reader.get_mes_for_lumi(run, lumi, "*")
            for me in me_list:
                if me.type not in self.H2D_VALID_MES:
                    continue

                entries = me.data.GetEntries()
                hist_x_bins = me.data.GetNbinsX()
                hist_y_bins = me.data.GetNbinsY()
                hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
                hist_x_max = me.data.GetXaxis().GetBinLowEdge(hist_x_bins) + me.data.GetXaxis().GetBinWidth(hist_x_bins)
                hist_y_min = me.data.GetYaxis().GetBinLowEdge(1)
                hist_y_max = me.data.GetYaxis().GetBinLowEdge(hist_y_bins) + me.data.GetYaxis().GetBinWidth(hist_y_bins)

                # data should be in the form of data[x][y]
                data = []
                for i in range(1, hist_y_bins + 1):
                    datarow = []
                    for j in range(1, hist_x_bins + 1):
                        datarow.append(me.data.GetBinContent(j, i))
                    data.append(datarow)

                run_obj, _ = Run.objects.get_or_create(run_number=me.run)
                lumi_obj, _ = Lumisection.objects.get_or_create(run=run_obj, ls_number=me.lumi)

                count_lumih2d = LumisectionHistogram2D.objects.filter(lumisection=lumi_obj, title=me.name).count()
                if count_lumih2d == 0:
                    h2d_list.append(
                        LumisectionHistogram2D(
                            lumisection=lumi_obj,
                            title=me.name,
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
                    )

            n_ingested = len(LumisectionHistogram2D.objects.bulk_create(h2d_list, ignore_conflicts=True))
            entries_ingested += n_ingested
            logger.debug(
                f"{n_ingested} x 2D lumisection histos successfully added from file {self.file_index.file_path}."
            )

            self.file_index.n_entries_ingested += n_ingested
            self.file_index.save()

            current_lumi += 1
            if read_chunk_lumi >= current_lumi:
                logger.debug(f"Read until requested lumi {read_chunk_lumi}, stopping")
                break

        return entries_ingested

    def run(self):
        """
        Ingest both H1D and H2D
        """
        try:
            self.file_index.update_status(FileIndexStatus.RUNNING)
            ingested_h1d_entries = self.__h1d()
            ingested_h2d_entries = self.__h2d()
            self.file_index.update_status(FileIndexStatus.PROCESSED)
        except Exception as err:
            self.file_index.update_status(FileIndexStatus.FAILED)
            raise err

        return {
            "h1d_entries": ingested_h1d_entries,
            "h2d_entries": ingested_h2d_entries,
        }
