from django.shortcuts import render
from django_tables2 import RequestConfig
from lumisection_histos1D.models import LumisectionHisto1D
from lumisection_histos1D.tables import LumisectionHisto1DTable
from lumisection_histos1D.api.filters import LumisectionHisto1DFilter


def listLumisectionHisto1D(request):
    """
    View to list the filtered 1D histograms for Lumisections
    """
    context = {}
    lumisectionHistos1D_list = LumisectionHisto1D.objects.all()
    lumisectionHistos1D_filter = LumisectionHisto1DFilter(
        request.GET, queryset=lumisectionHistos1D_list)
    lumisectionHistos1D_table = LumisectionHisto1DTable(
        lumisectionHistos1D_filter.qs[:50])

    RequestConfig(request).configure(lumisectionHistos1D_table)

    context["lumisectionHistos1D_table"] = lumisectionHistos1D_table
    context["filter"] = lumisectionHistos1D_filter
    return render(request, "lumisection_histos1D/listLumisectionHistos1D.html",
                  context)
