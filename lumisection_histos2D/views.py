from django.shortcuts import render
from django_tables2 import RequestConfig

from lumisection_histos2D.models import LumisectionHisto2D
from lumisection_histos2D.api.filters import LumisectionHisto2DFilter
from lumisection_histos2D.tables import LumisectionHisto2DTable


def listLumisectionHistos2D(request):
    """
    View to list the filtered 2D histograms for Lumisections
    """
    context = {}
    lumisectionHistos2D_list = LumisectionHisto2D.objects.all()
    lumisectionHistos2D_filter = LumisectionHisto2DFilter(
        request.GET, queryset=lumisectionHistos2D_list)
    lumisectionHistos2D_table = LumisectionHisto2DTable(
        lumisectionHistos2D_filter.qs[:50])

    RequestConfig(request).configure(lumisectionHistos2D_table)

    context["lumisectionHistos2D_table"] = lumisectionHistos2D_table
    context["filter"] = lumisectionHistos2D_filter
    return render(request, "lumisection_histos2D/listLumisectionHistos2D.html",
                  context)
