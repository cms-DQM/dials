from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django_tables2 import RequestConfig
from django_filters import rest_framework as filters

from runs.models import Run
from run_histos.models import RunHisto
from run_histos.tables import RunHistosTable1D
from run_histos.filters import RunHistos1DFilter
from run_histos.utilities.utilities import request_contains_filter_parameter
from run_histos.serializers import RunHistosSerializer

from run_histos.utils import get_altair_chart
import pandas as pd
import altair as alt

from rest_framework import generics
# Create your views here.

def listRunHistos1D(request):
    """
    View to list the filtered 1D histograms for Runs
    """
    context = {}
    runHistos_list = RunHisto.objects.all()
    runHistos_filter = RunHistos1DFilter(request.GET, queryset=runHistos_list)
    runHistos_table = RunHistosTable1D(runHistos_filter.qs[:50])

    RequestConfig(request).configure(runHistos_table)

    context["runHistos_table"] = runHistos_table
    context["filter"] = runHistos_filter
    return render(request, "run_histos/listRunHistos1D.html", context)

class listRunHistos1DAPI(generics.ListAPIView):
    queryset = RunHisto.objects.all()
    serializer_class = RunHistosSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RunHistos1DFilter

def import_view(request):
    return render(request, 'run_histos/import.html')

  
def run_histos_view(request):

    error_message = None
    dataset       = None
    variable      = None
    chart_type    = None
    df            = None
    mean          = None
    chart         = {}

    # objects.all().values() provides a dictionary while objects.all().values_list() provides a tuple
    runs_df      = pd.DataFrame(Run.objects.all().values())
    runhistos_df = pd.DataFrame(RunHisto.objects.all()[:200].values())

    if runhistos_df.shape[0] > 0:
        df = pd.merge(runs_df, runhistos_df, left_on='id', right_on='run_id').drop(['id_x', 'id_y', 'run_id', 'date_x', 'date_y'], axis=1)

        if request.method == 'POST':
            dataset   = request.POST['dataset']
            variable  = request.POST['variable']
            chart_type = request.POST['plot_type']
            print(f"dataset: {dataset} / variable: {variable} / chart_type: {chart_type}")

        #df = df.query('primary_dataset.str.lower()==@dataset & title.str.lower()==@variable')
        #df = df.query('primary_dataset==@dataset & title==@variable')
        mean = df['mean'].to_frame().to_html()

        chart = get_altair_chart(chart_type, df=df)

    else:
        error_message = "No runhistos in the database"

    context = {
        'error_message': error_message,
        'df':            df,
        'mean':          mean,
        'chart' :        chart,
    }

    return render(request, 'run_histos/main.html', context)

  
def altair_chart_view(request):

    chart = {}

    runhistos_df = pd.DataFrame(RunHisto.objects.all()[:200].values())

    if runhistos_df.shape[0] > 0:   
        chart_obj = alt.Chart(runhistos_df).mark_bar().encode(
            x='mean',
        ).to_json(indent=None)

    else:
        print("No runshistos in the database")

    return JsonResponse(chart_obj)


# class listRunHistos1DView(SingleTableMixin, FilterView):
#     table_class = RunHistosTable1D
#     model = RunHisto
#     template_name = "run_histos/listRunHistos1D.html"
#     filterset_class = RunHistos1DFilter
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         runHistos_list = RunHisto.objects.all()[:200]
#         runHistos_table = RunHistosTable1D(runHistos_list)
#         context["runHistos_table"] = runHistos_table
    
#         return context