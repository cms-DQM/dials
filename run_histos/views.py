from django.shortcuts import render
from runs.models import Run
from .models import RunHisto

import pandas as pd

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
            histogram = request.POST['histogram']
            print(f"histogram: {histogram}")

    else:
        error_message = "No records in the database"

    context = {
        'error_message': error_message,
        'df': df.to_html(),
    }

    return render(request, 'run_histos/main.html', context)
