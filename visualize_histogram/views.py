from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from data_taking_objects.models import Lumisection

from histograms.models import LumisectionHistogram1D, LumisectionHistogram2D
from .forms import QuickJumpForm

import data_taking_objects.views

import numpy as np

# Create your views here.

@login_required
def visualize_histogram(request, runnr, lumisection, title):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    if request.method == 'GET':
        form = QuickJumpForm(request.GET)
        if form.is_valid():
            runnr = form.cleaned_data["runnr"]
            lumisection = form.cleaned_data["lumisection"]
            title = form.cleaned_data["title"]
            return redirect("visualize_histogram:visualize_histogram",
                runnr=runnr, 
                lumisection=lumisection, 
                title=title
            )
        else: 
            form = QuickJumpForm(
                initial = {
                    "runnr": runnr,
                    "lumisection": lumisection,
                    "title": title
                }
            )
    else: 
        form = QuickJumpForm(
            initial = {
                "runnr": runnr,
                "lumisection": lumisection,
                "title": title
            }
        )

    try:
        target_lumi = Lumisection.objects.get(run_id = runnr, ls_number = lumisection)
        lumi1d_searchresults = LumisectionHistogram1D.objects.filter(title=title, lumisection=target_lumi)
        lumi2d_searchresults = LumisectionHistogram2D.objects.filter(title=title, lumisection=target_lumi)
        if len(lumi1d_searchresults) == 1: 
            histobj = lumi1d_searchresults[0]
            return render(
                request,
                "visualize_histogram/visualize_histogram.html",
                {
                    "data": histobj.data,
                    "bins": np.linspace(histobj.x_min, histobj.x_max, histobj.x_bin+1).tolist(), 
                    "title": histobj.title,
                    "runnr": target_lumi.run_id,
                    "lumisection": target_lumi.ls_number,
                    "form": form
                }
            )
        elif len(lumi2d_searchresults) == 1: 
            histobj = lumi2d_searchresults[0]
            return render(
                request,
                "visualize_histogram/visualize_histogram.html",
                {
                    "data2d": histobj.data,
                    "xbins": np.linspace(histobj.x_min, histobj.x_max, histobj.x_bin+1).tolist(), 
                    "ybins": np.linspace(histobj.y_min, histobj.y_max, histobj.y_bin+1).tolist(), 
                    "title": histobj.title,
                    "runnr": target_lumi.run_id,
                    "lumisection": target_lumi.ls_number,
                    "form": form
                }
            )
        else: 
            return render(
                request,
                "visualize_histogram/visualize_histogram.html",
                {"data": None, "runnr": runnr, "lumisection": lumisection, "title": title, "form": form}
            )
    except (Lumisection.DoesNotExist):
        # Return with no context
        return render(
            request,
            "visualize_histogram/visualize_histogram.html",
            {"data": None, "runnr": runnr, "lumisection": lumisection, "title": title, "form": form}
        )
    
@login_required
def visualize_histogram_dummy(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    if request.method == 'GET':
        form = QuickJumpForm(request.GET)
        if form.is_valid():
            runnr = form.cleaned_data["runnr"]
            lumisection = form.cleaned_data["lumisection"]
            title = form.cleaned_data["title"]
            return redirect("visualize_histogram:visualize_histogram",
                runnr=runnr, 
                lumisection=lumisection, 
                title=title
            )
        else: form = QuickJumpForm()
    else:
        form = QuickJumpForm()

    # dummy_hist = LumisectionHistogram1D.objects.latest("lumisection_id")
    # return redirect("visualize_histogram:visualize_histogram", runnr=dummy_hist.lumisection.run_id, 
    #     lumisection=dummy_hist.lumisection.ls_number, 
    #     title=dummy_hist.title
    # )
    print(request.GET)
    return render(request, "visualize_histogram/visualize_firstpage.html", {"form": form})

@login_required
def redirect_lumisection(request, runnr, lumisection):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    return data_taking_objects.views.lumisection_view(request, runnr, lumisection)

@login_required
def redirect_run(request, runnr):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    return data_taking_objects.views.run_view(request, runnr)