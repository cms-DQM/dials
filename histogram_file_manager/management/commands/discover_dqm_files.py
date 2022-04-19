# import re
import os
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Scans the default DQM datafile directory recursively for new files and"
        "stores them in the Database"
    )

    def handle(self, *args, **options):
        valid_files_extensions = [
            choice[0] for choice in HistogramDataFile.DATAFILE_FORMAT_CHOICES
        ]

        logger.debug(
            f"Getting recursive file list of directory {settings.DIR_PATH_EOS_CMSML4DC} ..."
        )
        for root, dirs, files in sorted(os.walk(settings.DIR_PATH_EOS_CMSML4DC)):

            for f in sorted(files):
                # Check if file has correct extension
                is_valid_extension = False
                for valid_extension in valid_files_extensions:
                    if f.endswith(valid_extension):
                        is_valid_extension = True
                        break

                if not is_valid_extension:
                    logger.debug(f"Invalid file extension on file {f}, skipping")
                    continue

                f = os.path.join(root, f)

                try:
                    hdf = HistogramDataFile.objects.get(filepath=f)
                    logger.debug(f"File '{hdf}' already in DB")
                except ObjectDoesNotExist:
                    logger.debug(f"File '{f}' not found in DB, creating new entry")
                    hdf = HistogramDataFile(filepath=f).save()
                    logger.info(f"Stored new file in DB: {hdf}")
