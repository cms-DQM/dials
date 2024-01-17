import logging

from django.http import HttpResponseBadRequest
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from dqmio_file_indexer.models import FileIndex

from .models import (
    Run,
    Lumisection,
    RunHistogram,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
    IngestHistogramsResponseBase
)
from .serializers import (
    DQMIORunSerializer,
    DQMIOLumisectionSerializer,
    DQMIORunHistogramSerializer,
    DQMIOLumisectionHistogram1DSerializer,
    DQMIOLumisectionHistogram2DSerializer,
    DQMIOLumisectionHistogram1DInputSerializer,
    DQMIOLumisectionHistogram2DInputSerializer,
    DQMIOLumisectionHistogramResponseSerializer,
)
from .reader import DQMIOReader

logger = logging.getLogger(__name__)


class DQMIORunViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Runs metadata
    """
    queryset = Run.objects.all().order_by("run_number")
    serializer_class = DQMIORunSerializer


class DQMIOLumisectionViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Lumisections metadata
    """
    queryset = Lumisection.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionSerializer


class DQMIORunHistogramViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested histograms at run granularity-level
    """
    queryset = RunHistogram.objects.all().order_by("id")
    serializer_class = DQMIORunHistogramSerializer

    # TODO
    # Action to trigger ETL pipeline for histograms at run granularity-level


class DQMIOLumisectionHistogram1DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 1d-histograms at lumisection granularity-level
    """
    queryset = LumisectionHistogram1D.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionHistogram1DSerializer

    @staticmethod
    def __ingest_function(file_index: FileIndex) -> int:
        # Load file in DQMIOReader and extract data
        dqmio_reader = DQMIOReader(file_index.file_path)
        entries_ingested = 0

        if file_index.n_entries == 0:
            file_index.n_entries = dqmio_reader.count_mes()
            file_index.save()

        for run_lumi_tuple in dqmio_reader.list_lumis():
            lumisection_histos_1d = []
            me_list = dqmio_reader.get_mes_for_lumi(run_lumi_tuple, "*")
            for me in me_list:
                if me.type not in (3, 4, 5):
                    continue
            
                entries = me.data.GetEntries()
                hist_x_bins = me.data.GetNbinsX()
                hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
                hist_x_max = me.data.GetXaxis().GetBinLowEdge(
                    hist_x_bins + 1
                )  # Takes low edge of overflow bin instead.
                data = [me.data.GetBinContent(i) for i in range(1, hist_x_bins + 1)]

                run_obj, _ = Run.objects.get_or_create(run_number=me.run)
                lumisection_obj, _ = Lumisection.objects.get_or_create(
                    run=run_obj, ls_number=me.lumi
                )

                count_lumih1d = LumisectionHistogram1D.objects.filter(lumisection=lumisection_obj, title=me.name).count()
                if count_lumih1d == 0:
                    lumisection_histo_1d = LumisectionHistogram1D(
                        lumisection=lumisection_obj,
                        title=me.name,
                        entries=entries,
                        data=data,
                        source_data_file=file_index,
                        x_min=hist_x_min,
                        x_max=hist_x_max,
                        x_bin=hist_x_bins,
                    )
                    lumisection_histos_1d.append(lumisection_histo_1d)

            n_ingested = len(LumisectionHistogram1D.objects.bulk_create(lumisection_histos_1d, ignore_conflicts=True))
            logger.info(f"{n_ingested} x 1D lumisection histos successfully added from file {file_index.file_path}.")

            # Make sure that the number of processed entries is 1D + 2D hists combined.
            file_index.n_entries_ingested += n_ingested
            file_index.save()

            entries_ingested += n_ingested

        return entries_ingested

    @extend_schema(
        request=DQMIOLumisectionHistogram1DInputSerializer,
        responses={200: DQMIOLumisectionHistogramResponseSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        name="Trigger ETL pipeline for 1d-histograms at lumisection granularity-level",
        url_path=r"ingest"
    )
    def run(self, request):
        file_index_id = request.data.get("id")
        if not file_index_id:
            return HttpResponseBadRequest("Attribute 'id' not found in request body.")

        # Load file index to extract metadata
        file_index = FileIndex.objects.get(id=file_index_id)

        # Try ingesting
        try:
            file_index.update_status("status_h1d", "running")
            entries_ingested = self.__ingest_function(file_index)
            file_index.update_status("status_h1d", "ok")
        except Exception as err:
            file_index.update_status("status_h1d", "failed")
            raise err

        payload = IngestHistogramsResponseBase(entries_ingested=entries_ingested)
        payload = DQMIOLumisectionHistogramResponseSerializer(payload)
        return Response(payload.data)


class DQMIOLumisectionHistogram2DViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested 2d-histograms at lumisection granularity-level
    """
    queryset = LumisectionHistogram2D.objects.all().order_by("id")
    serializer_class = DQMIOLumisectionHistogram2DSerializer

    @staticmethod
    def __ingest_function(file_index: FileIndex, read_chunk_lumi: int) -> int:
        # Load file in DQMIOReader and extract data
        dqmio_reader = DQMIOReader(file_index.file_path)
        entries_ingested = 0
        current_lumi = 0

        if file_index.n_entries == 0:
            file_index.n_entries = dqmio_reader.count_mes()
            file_index.save()

        for run_lumi_tuple in dqmio_reader.list_lumis():
            lumisection_histos_2d = []
            me_list = dqmio_reader.get_mes_for_lumi(run_lumi_tuple, "*")
            for me in me_list:
                if me.type not in (6, 7, 8):
                    continue

                entries = me.data.GetEntries()
                hist_x_bins = me.data.GetNbinsX()
                hist_y_bins = me.data.GetNbinsY()
                hist_x_min = me.data.GetXaxis().GetBinLowEdge(1)
                hist_x_max = me.data.GetXaxis().GetBinLowEdge(
                    hist_x_bins
                ) + me.data.GetXaxis().GetBinWidth(hist_x_bins)
                hist_y_min = me.data.GetYaxis().GetBinLowEdge(1)
                hist_y_max = me.data.GetYaxis().GetBinLowEdge(
                    hist_y_bins
                ) + me.data.GetYaxis().GetBinWidth(hist_y_bins)

                # data should be in the form of data[x][y]
                data = []
                for i in range(1, hist_y_bins + 1):
                    datarow = []
                    for j in range(1, hist_x_bins + 1):
                        datarow.append(me.data.GetBinContent(j, i))
                    data.append(datarow)

                run_obj, _ = Run.objects.get_or_create(run_number=me.run)
                lumisection_obj, _ = Lumisection.objects.get_or_create(
                    run=run_obj, ls_number=me.lumi
                )

                count_lumih2d = LumisectionHistogram2D.objects.filter(lumisection=lumisection_obj, title=me.name).count()
                if count_lumih2d == 0:
                    lumisection_histo_2d = LumisectionHistogram2D(
                        lumisection=lumisection_obj,
                        title=me.name,
                        entries=entries,
                        data=data,
                        source_data_file=file_index,
                        x_min=hist_x_min,
                        x_max=hist_x_max,
                        x_bin=hist_x_bins,
                        y_min=hist_y_min,
                        y_max=hist_y_max,
                        y_bin=hist_y_bins,
                    )
                    lumisection_histos_2d.append(lumisection_histo_2d)

            n_ingested = len(LumisectionHistogram2D.objects.bulk_create(lumisection_histos_2d, ignore_conflicts=True))
            logger.info(f"{n_ingested} x 2D lumisection histos successfully added from file {file_index.file_path}.")

            # Make sure that the number of processed entries is 1D + 2D hists combined.
            file_index.n_entries_ingested += n_ingested
            file_index.save()

            entries_ingested += n_ingested
            current_lumi += 1
            if read_chunk_lumi >= current_lumi:
                logger.info(f"Read until requested lumi {read_chunk_lumi}, stopping")
                break
        
        return entries_ingested

    @extend_schema(
        request=DQMIOLumisectionHistogram2DInputSerializer,
        responses={200: DQMIOLumisectionHistogramResponseSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        name="Trigger ETL pipeline for 2d-histograms at lumisection granularity-level",
        url_path=r"ingest"
    )
    def run(self, request):
        file_index_id = request.data.get("id")
        read_chunk_lumi = request.data.get("readUntilLumi", -1)
        if not file_index_id:
            return HttpResponseBadRequest("Attribute 'id' not found in request body.")

        # Load file index to extract metadata
        file_index = FileIndex.objects.get(id=file_index_id)
        
        # Try ingesting
        try:
            file_index.update_status("status_h2d", "running")
            entries_ingested = self.__ingest_function(file_index, read_chunk_lumi)
            file_index.update_status("status_h2d", "ok")
        except Exception as err:
            file_index.update_status("status_h2d", "failed")
            raise err
        
        payload = IngestHistogramsResponseBase(entries_ingested=entries_ingested)
        payload = DQMIOLumisectionHistogramResponseSerializer(payload)
        return Response(payload.data)
