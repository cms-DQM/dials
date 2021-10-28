from django.shortcuts import render
from django.http import JsonResponse

from runs.models import Run
from .models import RunHisto

from .utils import get_altair_chart

import pandas as pd
import altair as alt

# Create your views here.

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
    runhistos_df = pd.DataFrame(RunHisto.objects.all().values())

    if runhistos_df.shape[0] > 0:
        df = pd.merge(runs_df, runhistos_df, left_on='id', right_on='run_id').drop(['id_x', 'id_y', 'run_id', 'date_x', 'date_y'], axis=1)

        if request.method == 'POST':
            dataset   = request.POST['dataset']
            variable  = request.POST['variable']
            chart_type = request.POST['plot_type']
            print(f"dataset: {dataset} / variable: {variable} / chart_type: {chart_type}")

        # df = df.query('primary_dataset.str.lower()=="zerobias" & title.str.lower()=="chi2prob_gentk"')
        df = df.query('primary_dataset.str.lower()==@dataset & title.str.lower()==@variable')
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

    runhistos_df = pd.DataFrame(RunHisto.objects.all().values()).head(100)

    if runhistos_df.shape[0] > 0:   
        chart_obj = alt.Chart(runhistos_df).mark_bar().encode(
            x='mean',
        ).to_json(indent=None)

    else:
        print("No runshistos in the database")

    return JsonResponse(chart_obj)
