from django.shortcuts import render
from django.http import JsonResponse

from runs.models import Run
from .models import RunHisto

import pandas as pd
import altair as alt

from vega_datasets import data

# Create your views here.

def chart_select_view(request):

    error_message = None

    # objects.all().values() provides a dictionary while objects.all().values_list() provides a tuple
    runs_df      = pd.DataFrame(Run.objects.all().values())
    runhistos_df = pd.DataFrame(RunHisto.objects.all().values())

    if runhistos_df.shape[0] > 0:
        df = pd.merge(runs_df, runhistos_df, left_on='id', right_on='run_id').drop(['id_x', 'id_y', 'run_id', 'date_x', 'date_y'], axis=1).head(20)

        if request.method == 'POST':
            print(f"request.POST is {request.POST}")
            dataset   = request.POST['dataset']
            variable  = request.POST['variable']
            plot_type = request.POST['plot_type']
            print(f"dataset: {dataset} / variable: {variable} / plot_type: {plot_type}")

    else:
        error_message = "No records in the database"

    chart = alt.Chart(runhistos_df.head(100)).mark_bar().encode(
        x='mean',
    ).to_json(indent=None)

    context = {
        'error_message': error_message,
        'df':            df.to_html(),
        'chart' :        chart,
    }

    return render(request, 'run_histos/main.html', context)

def chart_view_altair(request):
    runhistos_df = pd.DataFrame(RunHisto.objects.all().values()).head(100)
    chart_obj = alt.Chart(runhistos_df).mark_bar().encode(
        x='mean',
    ).to_json(indent=None)
    return JsonResponse(chart_obj)
