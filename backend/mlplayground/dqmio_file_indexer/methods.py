import logging
import re
from datetime import datetime
from pathlib import Path

import ROOT
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
        fpath = str(file)
        with ROOT.TFile(fpath) as root_file:
            file_uuid = root_file.GetUUID().AsString()

        file_index, created = FileIndex.objects.get_or_create(
            file_uuid=file_uuid,
            file_path=fpath,
            data_era=RawDataIndexer.__infer_data_era(file.name),
            st_size=lstat.st_size,
            st_ctime=datetime.fromtimestamp(lstat.st_ctime, tz=timezone.get_current_timezone()),
        )

        # Do not return anything, next function will check if returned value is None
        if created is False:
            logger.debug(f"File {file} already exists in the database!")
            return

        logger.debug(f"Indexed new file in DB: {file}")
        return file_index.id

    @staticmethod
    def __search_dqmio_files(storage_dir):
        path = Path(storage_dir)
        files = [file for file in path.rglob("*") if file.suffix in FileIndex.VALID_FILE_EXTS and file.is_file()]
        total_files = len(files)
        files = [RawDataIndexer.__index_file_in_database(file) for file in files]
        indexed_files_id = [file_id for file_id in files if file_id is not None]
        return {
            "total_files": total_files,
            "total_added_files": len(indexed_files_id),
            "indexed_files_id": indexed_files_id,
        }

    def start(self):
        stats = []
        for dir in self.STORAGE_DIRS:
            logger.debug(f"Getting recursive file list for path '{dir}'")
            dir_result = RawDataIndexer.__search_dqmio_files(dir)
            stats.append(
                FileIndexResponseBase(
                    storage=dir,
                    total=dir_result["total_files"],
                    added=dir_result["total_added_files"],
                    ingested_ids=dir_result["indexed_files_id"],
                )
            )
        return stats
