import logging
from django.core.management.base import BaseCommand

# from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from histogram_file_manager.models import HistogramDataFile
from histogram_file_manager.forms import HistogramDataFileForm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ("Scans the default DQM datafile directory for new files and"
            "stores them in the Database")

    def handle(self, *args, **options):
        # Use the form's FilePathField method to populate valid files
        for f in HistogramDataFileForm().fields.get("filepath")._choices:
            try:
                hdf = HistogramDataFile.objects.get(filepath=f[0])
                logger.debug(f"File '{hdf}' already in DB")
            except ObjectDoesNotExist:
                logger.debug(
                    f"File '{f[0]}' not found in DB, creating new entry")
                hdf = HistogramDataFile(filepath=f[0]).save()
                logger.info(f"Stored new file in DB: {hdf}")
