from django.shortcuts import render
from .models import Run

import pandas as pd

# Create your views here.

def chart_select_view(request):
    # objects.all().values() provides a dictionary while objects.all().values_list() provides a tuple
    runs_df = pd.DataFrame(Run.objects.all().values()).drop(['id'], axis=1)
    context = {
        'runs': runs_df.to_html(),
    }
    return render(request, 'runs/main.html', context)
