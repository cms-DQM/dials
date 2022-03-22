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

    # No need for custom path, always use the default one
    # def add_arguments(self, parser):
    #     parser.add_argument("directory",
    #                         nargs='?',
    #                         type=str,
    #                         default=settings.DIR_PATH_EOS_CMSML4DC)

    def handle(self, *args, **options):
        # directory_path = options["directory"]

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
