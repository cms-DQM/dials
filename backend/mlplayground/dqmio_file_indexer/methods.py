import logging
import re
from datetime import datetime
from pathlib import Path

import ROOT
from django.conf import settings
from django.utils import timezone
from dqmio_etl.tasks import ingest_function

from .models import BadFileIndex, FileIndex, FileIndexStatus

logger = logging.getLogger(__name__)


class RawDataIndexer:
    STORAGE_DIRS = settings.DIR_PATH_DQMIO_STORAGE.split(":")

    def __init__(self):
        self.indexed = None

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

        try:
            with ROOT.TFile(fpath) as root_file:
                file_uuid = root_file.GetUUID().AsString()
            file_is_bad = False
        except Exception as err:
            file_is_bad = True
            err_type = type(err).__name__
            parsed_err_text = str(err).replace(fpath, "<<fpath>>")
            err_msg = f"{err_type}: {parsed_err_text}"

        data_era = RawDataIndexer.__infer_data_era(file.name)
        st_ctime = datetime.fromtimestamp(lstat.st_ctime, tz=timezone.get_current_timezone())

        if file_is_bad:
            bad_file_index, created = BadFileIndex.objects.get_or_create(
                file_path=fpath, data_era=data_era, st_size=lstat.st_size, st_ctime=st_ctime, err=err_msg
            )
            return ("BAD", bad_file_index.id, created)

        file_index, created = FileIndex.objects.get_or_create(
            file_uuid=file_uuid,
            file_path=fpath,
            data_era=data_era,
            st_size=lstat.st_size,
            st_ctime=st_ctime,
        )

        if created is False:
            logger.debug(f"File {file} already exists in the database!")
        else:
            logger.debug(f"Indexed new file in DB: {file}")

        return ("GOOD", file_index.id, created)

    @staticmethod
    def __search_dqmio_files(storage_dir):
        path = Path(storage_dir)
        files = [file for file in path.rglob("*") if file.suffix in FileIndex.VALID_FILE_EXTS and file.is_file()]
        total_files = len(files)
        files = [RawDataIndexer.__index_file_in_database(file) for file in files]
        good_indexed_files_id = [
            file_id for file_status, file_id, created in files if created and file_status == "GOOD"
        ]
        bad_indexed_files_id = [file_id for file_status, file_id, created in files if created and file_status == "BAD"]
        return {
            "total_files": total_files,
            "total_added_good_files": len(good_indexed_files_id),
            "total_added_bad_files": len(bad_indexed_files_id),
            "good_indexed_files_id": good_indexed_files_id,
            "bad_indexed_files_id": bad_indexed_files_id,
        }

    def start(self):
        stats = []
        for dir in self.STORAGE_DIRS:
            logger.debug(f"Getting recursive file list for path '{dir}'")
            dir_result = RawDataIndexer.__search_dqmio_files(dir)
            stats.append(
                {
                    "storage": dir,
                    "total": dir_result["total_files"],
                    "added_good": dir_result["total_added_good_files"],
                    "added_bad": dir_result["total_added_bad_files"],
                    "good_ingested_ids": dir_result["good_indexed_files_id"],
                    "bad_ingested_ids": dir_result["bad_indexed_files_id"],
                }
            )
        self.indexed = stats

    def schedule_ingestion(self):
        response = {"n_scanned": 0, "n_indexed_good": 0, "n_indexed_bad": 0, "n_scheduled": 0}
        for dir_result in self.indexed:
            total_added_good = dir_result["added_good"]
            good_ingested_ids = dir_result["good_ingested_ids"]
            response["n_scanned"] += dir_result["total"]
            response["n_indexed_good"] += dir_result["added_good"]
            response["n_indexed_bad"] += dir_result["added_bad"]
            if total_added_good == 0:
                continue

            for ingested_id in good_ingested_ids:
                file_index = FileIndex.objects.get(id=ingested_id)
                file_index.update_status(FileIndexStatus.PENDING)
                del file_index
                ingest_function.delay(ingested_id)
                response["n_scheduled"] += 1
        return response
