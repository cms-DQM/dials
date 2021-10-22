from django.shortcuts import render
from .models import Run

import pandas as pd

# Create your views here.

def chart_select_view(request):
    # objects.all().values() provides a dictionary while objects.all().values_list() provides a tuple
    runs_df = pd.DataFrame(Run.objects.all().values())
    context = {
        'runs': runs_df,
    }
    return render(request, 'runs/main.html', context)
