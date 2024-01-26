from pathlib import Path
from datetime import datetime
import logging
import re

from django.conf import settings
from django.utils import timezone

from .models import FileIndex, FileIndexResponseBase

logger = logging.getLogger(__name__)


class RawDataIndexer:
    STORAGE_DIRS = settings.DIR_PATH_DQMIO_STORAGE.split(":")
    
    @staticmethod
    def __infer_era_from_string(era_string):
        if len(era_string) == 8 and "Run" in era_string:
            era_tmp = era_string.replace("Run", "")
            return RawDataIndexer.__infer_era_from_string(era_tmp)
        elif len(era_string) == 5:
            era_nums = era_string[:4]
            era_lett = era_string[4:]
            if era_nums.isdigit():
                try:
                    int(era_lett)
                except ValueError:
                    return era_string

    @staticmethod
    def __search_era_with_split(filename):
        try:
            era_string = filename.split("_")[2].strip()
        except IndexError:
            return None
        else:
            return RawDataIndexer.__infer_era_from_string(era_string)
        
    @staticmethod
    def __search_era_with_regex(filename):
        try:
            era_string = re.search(r"Run(\d+[A-Z])", filename).groups()[0]
        except Exception:
            return None
        else:
            return RawDataIndexer.__infer_era_from_string(era_string)

    @staticmethod
    def __infer_data_era(filename):
        era = RawDataIndexer.__search_era_with_split(filename)
        if era:
            return era

        era = RawDataIndexer.__search_era_with_regex(filename)
        if era:
            return era
        
        return "Unknown"

    @staticmethod
    def __index_file_in_database(file):
        lstat = file.lstat()
        _, created = FileIndex.objects.get_or_create(
            file_path=str(file),
            data_era=RawDataIndexer.__infer_data_era(file.name),
            st_size=lstat.st_size,
            st_ctime=datetime.fromtimestamp(lstat.st_ctime, tz=timezone.get_current_timezone())
        )
        message = f"Indexed new file in DB: {file}" if created else f"File {file} already exists in the database!"
        logger.debug(message)
        return int(created)

    @staticmethod
    def __search_dqmio_files(storage_dir):
        path = Path(storage_dir)
        files = [file for file in path.rglob("*") if file.suffix in FileIndex.VALID_FILE_EXTS and file.is_file()]
        files = [RawDataIndexer.__index_file_in_database(file) for file in files]
        return sum(files), len(files)

    def start(self):
        stats = []
        for dir in self.STORAGE_DIRS:
            logger.debug(f"Getting recursive file list for path '{dir}'")
            added_files, total_files = RawDataIndexer.__search_dqmio_files(dir)
            stats.append(FileIndexResponseBase(storage=dir, total=total_files, added=added_files))
        return stats
