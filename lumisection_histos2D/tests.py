import os
import os.path
import logging
import pandas as pd
from django.test import TestCase
from .models import LumisectionHisto2D
from histogram_file_manager.models import HistogramDataFile

logger = logging.getLogger(__name__)


class CSVHistogram2DParsingTestCase(TestCase):
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
                             "test_files", "per_lumi"))
            if os.path.isfile(os.path.join(self.test_files_directory, f))
        ]

        # Create entries in db
        for f in files:
            # Count lines of CSV
            self.num_total_lines += pd.read_csv(f).shape[0]
            LumisectionHisto2D.from_csv(file_path=f)

    def test_csv_histogram_1d_parsing(self):
        logger.debug(f"There are {LumisectionHisto2D.objects.count()} "
                     "2D Lumisection histograms in the DB")
        # Stupid test to verify that 9 histograms were loaded from one file
        assert LumisectionHisto2D.objects.count() == self.num_total_lines
