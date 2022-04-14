import os
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ("Scans the default DQM datafile directory for new files and"
            "stores them in the Database")

    def handle(self, *args, **options):
        for root, dirs, files in sorted(os.walk(
                settings.DIR_PATH_EOS_CMSML4DC)):
            for f in sorted(files):
                f = os.path.join(root, f)
                try:
                    hdf = HistogramDataFile.objects.get(filepath=f)
                    logger.debug(f"File '{hdf}' already in DB")
                except ObjectDoesNotExist:
                    logger.debug(
                        f"File '{f[0]}' not found in DB, creating new entry")
                    hdf = HistogramDataFile(filepath=f).save()
                    logger.info(f"Stored new file in DB: {hdf}")
