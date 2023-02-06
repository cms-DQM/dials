from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def visualize_histogram(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    # Convert all available choices to a dict so that JS can understand it

    return render(
        request,
        "visualize_histogram/visualize_histogram.html"
    )
