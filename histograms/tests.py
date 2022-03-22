import os
import os.path
import logging
# import threading
import pandas as pd
from django.test import TestCase
# from django.core import management
from histograms.models import LumisectionHistogram1D, LumisectionHistogram2D
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)


class CSVHistogram1DParsingTestCase(TestCase):
    """
    Test parsing a 1D Histogram CSV file and storing it into the DB
    """
    test_files_directory = ""
    test_files = []
    num_total_lines = 0  # Total lines across all test files

    def setUp(self):
        # List all files in the test_files/per_lumi directory
        self.test_files_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_files", "1D",
            "per_lumi")
        self.test_files = [
            os.path.join(self.test_files_directory, f) for f in os.listdir(
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "test_files", "per_lumi"))
            if os.path.isfile(os.path.join(self.test_files_directory, f))
        ]

        # Create entries in db
        for f in self.test_files:
            # Count lines of CSV
            self.num_total_lines += pd.read_csv(f).shape[0]
            LumisectionHistogram1D.from_csv(file_path=f)

    def test_csv_histogram_1d_parsing(self):
        logger.debug(f"There are {LumisectionHistogram1D.objects.count()} "
                     "1D Lumisection histograms in the DB")

        # Assumes all lines in all CSV test files are unique
        assert LumisectionHistogram1D.objects.count() == self.num_total_lines
        for hdf in HistogramDataFile.objects.all():
            assert hdf.percentage_processed == 100.0


class CSVHistogram2DCompleteParsingTestCase(TestCase):
    """
    Test parsing a 2D Histogram CSV file and storing it into the DB
    """
    test_files_directory = ""
    test_files = []
    num_total_lines = 0  # Total lines across all test files

    def setUp(self):
        # List all files in the test_files/per_lumi directory
        self.test_files_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_files",
            "per_lumi")
        files = [
            os.path.join(self.test_files_directory, f) for f in os.listdir(
                os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "test_files", "2D", "per_lumi"))
            if os.path.isfile(os.path.join(self.test_files_directory, f))
        ]

        # Create entries in db
        for f in files:
            # Count lines of CSV
            self.num_total_lines += pd.read_csv(f).shape[0]
            LumisectionHistogram2D.from_csv(file_path=f)

    def test_csv_histogram_2d_parsing_completeness(self):
        logger.debug(f"There are {LumisectionHistogram2D.objects.count()} "
                     "2D Lumisection histograms in the DB")
        assert LumisectionHistogram2D.objects.count() == self.num_total_lines
        for hdf in HistogramDataFile.objects.all():
            # logger.debug(f"{hdf.filepath}\t{hdf.percentage_processed}")
            assert hdf.percentage_processed == 100.0


# TODO: Add test which partially stores a Histogram file, then tries to resume
# and verifies that it was added completely. Possible ways to do it:
# 1) Call the management command as a Thread, which will have to be killed
# somehow after some arbitrary time delay.
# 2) Call the management command as a subprocess. This requires that the venv
# is somehow activated first. Then, a SIGKILL should suffice.
# 3) Modify the from_file method to accept a limit to the lines it reads, so
# that the file is incompletely read.
