from django.shortcuts import render

from runs.models import Run
from run_histos.models import RunHisto

import pandas as pd
import numpy as np
import altair as alt


# Create your views here.
def run_certification_view(request):
    return render(request, 'run_certification/main.html')
