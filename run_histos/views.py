from django.shortcuts import render
from run_histos.models import RunHisto
from dataset_tables.tables import RunHistoTable1D

# Create your views here.


def listRunHistos1D(request):
    """
    View to list all 1D histograms for Run based data
    """
    context = {}

    runHistos_list = RunHisto.objects.all()[:200]
    runHistos_table = RunHistoTable1D(runHistos_list)
    context["runHistos_table"] = runHistos_table

    return render(request, "run_histos/listRunHistos1D.html", context)