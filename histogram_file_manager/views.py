import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileForm
from histogram_file_manager.tables import HistogramDataFileTable

logger = logging.getLogger(__name__)


@login_required
def histogram_file_manager(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """
    context = {}
    all_files = HistogramDataFileForm().fields.get('filepath')._choices

    # Populate the table with data
    table = HistogramDataFileTable.from_filepaths(all_files)
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
