from django.shortcuts import render

from data_taking_objects.models import Run
from histograms.models import RunHistogram

import pandas as pd
import numpy as np
import altair as alt


# Create your views here.
def run_certification_view(request):
    return render(request, 'run_certification/main.html')
