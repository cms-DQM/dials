import logging
from django.shortcuts import render
from .models import HistogramDataFile
from .forms import FileManagerForm

logger = logging.getLogger(__name__)


def histogram_file_manager(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """
    context = {}
    data_files = HistogramDataFile.objects.all()
    context['data_files'] = data_files
    if request.method == 'POST':
        logger.debug("POST")
    else:
        logger.debug("OMG GET")
        context['form'] = FileManagerForm()

    return render(request,
                  'histogram_file_manager/histogram_file_manager.html',
                  context=context)
