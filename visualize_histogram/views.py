from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from data_taking_objects.models import Lumisection

from histograms.models import LumisectionHistogram1D, LumisectionHistogram2D
import numpy as np

# Create your views here.

@login_required
def visualize_histogram(request, runnr, lumisection, title):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    # Convert all available choices to a dict so that JS can understand it
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
                    "lumisection": target_lumi.ls_number
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
                    "lumisection": target_lumi.ls_number
                }
            )
        else: 
            histobj = None
            return render(
                request,
                "visualize_histogram/visualize_histogram.html",
                {"data": None, "runnr": runnr, "lumisection": lumisection, "title": title}
            )
    except (Lumisection.DoesNotExist):
        # Return with no context
        render(
            request,
            "visualize_histogram/visualize_histogram.html",
            {"data": None}
        )
    
@login_required
def visualize_histogram_dummy(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    # Convert all available choices to a dict so that JS can understand it
    dummy_hist = LumisectionHistogram1D.objects.latest("lumisection_id")
    #return redirect("visualize_histogram", runnr=dummy_hist.lumisection.run_id, 
    #    lumisection=dummy_hist.lumisection.ls_number, 
    #    title=dummy_hist.title
    #)
    return visualize_histogram(request, runnr=dummy_hist.lumisection.run_id, 
        lumisection=dummy_hist.lumisection.ls_number, 
        title=dummy_hist.title)