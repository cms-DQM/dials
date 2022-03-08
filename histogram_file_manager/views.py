import logging
from django.shortcuts import render
from .models import HistogramDataFile
from .forms import HistogramDataFileForm
from .tables import HistogramDataFileTable

logger = logging.getLogger(__name__)


def histogram_file_manager(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """
    context = {}
    all_files = HistogramDataFileForm().fields.get('filepath')._choices
    files_in_db = HistogramDataFile.objects.all()

    # Populate the table with data
    table = HistogramDataFileTable([{
        "filepath":
        f[0],
        "in_db":
        bool(len(files_in_db.filter(filepath=f[0])) == 1)
    } for f in all_files])
    context['files_in_db'] = files_in_db
    context['table'] = table

    # Populate list of available DQM histogram files

    # if request.method == 'POST':
    #     pass
    # else:
    #     # FilePathField choices returns a tuple with the full path and the filename
    #     context['file_choices'] = {
    #         f[1]: {
    #             'in_db': bool(len(files_in_db.filter(filepath=f[0])) == 1)
    #         }
    #         for f in all_files
    #     }

    return render(request,
                  'histogram_file_manager/histogram_file_manager.html',
                  context=context)
