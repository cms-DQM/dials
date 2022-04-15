import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileStartParsingForm
from histogram_file_manager.api.filters import HistogramDataFileFilter

logger = logging.getLogger(__name__)


@login_required
def histogram_file_manager(request):
    """
    View for histogram file manager. Lists all available datafiles and their
    parsing status
    """

    # Convert all available choices to a dict so that JS can understand it
    field_choices = {
        field: dict(choices.choices)
        for field, choices in
        HistogramDataFileStartParsingForm().fields.items()
    }

    # Get filter to render on front-end
    hdf_filter = HistogramDataFileFilter(
        request.GET, queryset=HistogramDataFile.objects.all())

    return render(request,
                  'histogram_file_manager/histogram_file_manager.html',
                  context={
                      'field_choices': field_choices,
                      'filter': hdf_filter
                  })
