import os
import os.path
import logging
import pandas as pd
from django.test import TestCase
from .models import LumisectionHisto1D
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
            os.path.dirname(os.path.abspath(__file__)), "test_files",
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
            LumisectionHisto1D.from_csv(file_path=f)

    def test_csv_histogram_1d_parsing(self):
        logger.debug(f"There are {LumisectionHisto1D.objects.count()} "
                     "1D Lumisection histograms in the DB")

        # Assumes all lines in all CSV test files are unique
        assert LumisectionHisto1D.objects.count() == self.num_total_lines
        for hdf in HistogramDataFile.objects.all():
            assert hdf.percentage_processed == 100.0
