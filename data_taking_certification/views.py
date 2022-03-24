import pandas as pd
import numpy as np
import altair as alt
from django.shortcuts import render
from data_taking_objects.models import Run
from histograms.models import RunHistogram


# Create your views here.
def run_certification_view(request):
    return render(request, 'data_taking_certification/runs_main.html')
