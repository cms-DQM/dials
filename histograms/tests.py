import os
import os.path
import math
import logging

# import threading
import pandas as pd
from django.test import TestCase
from unittest import skipIf

# from django.core import management
from histograms.models import (
    LumisectionHistogram1D,
    LumisectionHistogram2D,
    LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE,
)
from histogram_file_manager.models import HistogramDataFile

if not os.environ.get("GITHUB_WORKFLOW"): import histograms.DQMIOReader

logger = logging.getLogger(__name__)


class CSVHistogram1DParsingTestCase(TestCase):
    """
    Test parsing a 1D Histogram CSV file and storing it into the DB
    """

    test_files_directory = ""
    test_files = []
    num_total_lines = 0  # Total lines across all test files

    def setUp(self):
        self.num_total_lines = 0  # Reset, this method will be called again
        # List all files in the test_files/per_lumi directory
        self.test_files_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_files", "1D", "per_lumi"
        )
        self.test_files = [
            os.path.join(self.test_files_directory, f)
            for f in os.listdir(self.test_files_directory)
            if os.path.isfile(os.path.join(self.test_files_directory, f))
            and os.path.splitext(f)[1] == ".csv" # Make sure the file tested is actually CSV.
        ]

        # Create entries in db
        for f in self.test_files:
            # Count lines of CSV
            self.num_total_lines += pd.read_csv(f).shape[0]
            LumisectionHistogram1D.from_csv(file_path=f)

    def test_csv_histogram_1d_parsing(self):
        logger.debug(
            f"There are {LumisectionHistogram1D.objects.count()} "
            "1D Lumisection histograms in the DB"
        )

        # Assumes all lines in all CSV test files are unique
        assert LumisectionHistogram1D.objects.count() == self.num_total_lines
        for hdf in HistogramDataFile.objects.all():
            assert hdf.percentage_processed == 100.0

    def test_duplicate_entries(self):
        """
        Make sure that re-reading the same CSV will not lead to duplicate entries
        """
        # Try to re-read 1D csv files
        self.setUp()

        # Should not have changed
        assert LumisectionHistogram1D.objects.count() == self.num_total_lines

#class NanoDQMHistogram1DParsingTestCase(TestCase):
#    """
#    Test parsing a 1D Histogram NanoDQM file and storing it into the DB
#    This test class is a duplicate of CSVHistogram1DParsingTestCase.
#    """
#
#    test_files_directory = ""
#    test_files = []
#    num_total_entries = 0  # Total lines across all test files
#
#    def setUp(self):
#        self.num_total_entries = 0  # Reset, this method will be called again
#        # List all files in the test_files/nanodqmio directory
#        self.test_files_directory = os.path.join(
#            os.path.dirname(os.path.abspath(__file__)), "test_files", "nanodqmio"
#        )
#        self.test_files = [
#            os.path.join(self.test_files_directory, f)
#            for f in os.listdir(self.test_files_directory)
#            if os.path.isfile(os.path.join(self.test_files_directory, f))
#            and os.path.splitext(f)[1] == ".root" # Make sure the file tested is actually ROOT.
#        ]
#
#        # Create entries in db
#        for f in self.test_files:
#            reader = histograms.DQMIOReader.DQMIOReader(f)
#            for run_fromreader, lumi_fromreader in reader.listLumis():
#                lumisection_histos1D = []
#                melist = reader.getMEsForLumi((run_fromreader, lumi_fromreader), "*")
#                for me in melist:
#                    if me.type in [3, 4, 5]: lumisection_histos1D.append(melist)
#                self.num_total_entries += len(lumisection_histos1D)
#            LumisectionHistogram1D.from_nanodqm(file_path=f)
#
#    # One file of nanoDQMIO may contain 1D and 2D histograms.
#    # Percentage processed
#
#    # def test_nanodqm_histogram_1d_parsing(self):
#    #     logger.debug(
#    #         f"There are {LumisectionHistogram1D.objects.count()} "
#    #         "1D Lumisection histograms in the DB"
#    #     )
#    # 
#    #     # Assumes all lines in all NanoDQM test files are unique
#    #     assert LumisectionHistogram1D.objects.count() == self.num_total_entries
#    #     for hdf in HistogramDataFile.objects.all():
#    #         assert hdf.percentage_processed == 100.0
#
#    def test_duplicate_entries(self):
#        """
#        Make sure that re-reading the same ROOT will not lead to duplicate entries
#        """
#        # Try to re-read 1D NanoDQM files
#        self.setUp()
#
#        # Should not have changed
#        assert LumisectionHistogram1D.objects.count() == self.num_total_entries

class CSVHistogram2DCompleteParsingTestCase(TestCase):
    """
    Test parsing a 2D Histogram CSV file and storing it into the DB
    """

    test_files_directory = ""
    test_files = []
    num_total_lines = 0  # Total lines across all test files

    def setUp(self):
        self.num_total_lines = 0
        # List all files in the test_files/per_lumi directory
        self.test_files_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_files", "2D", "per_lumi"
        )
        self.test_files = [
            os.path.join(self.test_files_directory, f)
            for f in os.listdir(self.test_files_directory)
            if os.path.isfile(os.path.join(self.test_files_directory, f))
            and os.path.splitext(f)[1] == ".csv" # Make sure the file tested is actually CSV.
        ]

    @staticmethod
    def _clear_db():
        LumisectionHistogram2D.objects.all().delete()
        HistogramDataFile.objects.all().delete()

    def _fillup_db(self):
        self.num_total_lines = 0
        # Create entries in db
        for f in self.test_files:
            # Count lines of CSV
            self.num_total_lines += pd.read_csv(f).shape[0]
            LumisectionHistogram2D.from_csv(file_path=f)

    def test_csv_histogram_2d_parsing_resumption(self):
        """
        Try to partially read only 1 chunk from a 2D CSV.
        Verify the percentage processed and then read the remaining.
        """
        self._clear_db()

        test_file = self.test_files[0]
        num_lines = pd.read_csv(test_file).shape[0]
        LumisectionHistogram2D.from_csv(file_path=test_file, read_chunk_num_max=1)

        test_file_db = HistogramDataFile.objects.get(filepath=test_file)
        assert math.isclose(
            test_file_db.percentage_processed,
            100 * (LUMISECTION_HISTOGRAM_2D_CHUNK_SIZE / num_lines),
            abs_tol=0.1,
        )

        # Read all the file
        LumisectionHistogram2D.from_csv(file_path=test_file)
        test_file_db = HistogramDataFile.objects.get(filepath=test_file)
        assert test_file_db.percentage_processed == 100.0

    def test_csv_histogram_2d_parsing_completeness(self):
        """
        Read all the available test files, and try to parse them into
        LumisectionHistogram2D entries. Make sure they're parsed to completion
        """
        self._clear_db()
        self._fillup_db()

        logger.debug(
            f"There are {LumisectionHistogram2D.objects.count()} "
            "2D Lumisection histograms in the DB"
        )
        assert LumisectionHistogram2D.objects.count() == self.num_total_lines
        for hdf in HistogramDataFile.objects.all():
            # logger.debug(f"{hdf.filepath}\t{hdf.percentage_processed}")
            assert hdf.percentage_processed == 100.0

    def test_duplicate_entries(self):
        """
        Make sure that re-reading the same CSV will not lead to duplicate entries
        """
        self._clear_db()
        # Fillup db twice
        self._fillup_db()
        self._fillup_db()

        # Should not have changed
        assert LumisectionHistogram2D.objects.count() == self.num_total_lines

class NanoDQMHistogramCompleteParsingTestCase(TestCase):
    """
    Test parsing a nanoDQM file and storing it into the DB
    A typical nanoDQM contains both 1D and 2D histograms, 
    so it should be parsed at the same time before checking for percentages.
    """

    test_files_directory = ""
    test_files = []
    num_total_entries = 0  # Total lines across all test files

    def setUp(self):
        self.num_total_entries = 0
        # List all files in the test_files/per_lumi directory
        self.test_files_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_files", "nanodqmio"
        )
        self.test_files = [
            os.path.join(self.test_files_directory, f)
            for f in os.listdir(self.test_files_directory)
            if os.path.isfile(os.path.join(self.test_files_directory, f))
            and os.path.splitext(f)[1] == ".root" # Make sure the file tested is actually ROOT.
        ]

    @staticmethod
    def _clear_db():
        LumisectionHistogram2D.objects.all().delete()
        HistogramDataFile.objects.all().delete()
    
    @staticmethod
    def count_mes(f, dimensions=-1):
        num_total_entries = 0
        reader = histograms.DQMIOReader.DQMIOReader(f)
        for run_fromreader, lumi_fromreader in reader.listLumis():
            melist = reader.getMEsForLumi((run_fromreader, lumi_fromreader), "*")
            for me in melist:
                if dimensions == 1:
                    if me.type in [3, 4, 5]: num_total_entries += 1
                elif dimensions == 2:
                    if me.type in [6, 7, 8]: num_total_entries += 1
                else:
                    if me.type in [3, 4, 5, 6, 7, 8]: num_total_entries += 1
        return num_total_entries

    @staticmethod
    def count_mes_first_lumi(f, dimensions=-1):
        num_total_entries = 0
        reader = histograms.DQMIOReader.DQMIOReader(f)
        firstrun, firstlumi = reader.listLumis()[0]
        melist = reader.getMEsForLumi((firstrun, firstlumi), "*")
        for me in melist:
            if dimensions == 1:
                if me.type in [3, 4, 5]: num_total_entries += 1
            elif dimensions == 2:
                if me.type in [6, 7, 8]: num_total_entries += 1
            else: 
                if me.type in [3, 4, 5, 6, 7, 8]: num_total_entries += 1
        return num_total_entries

    def _fillup_db(self):
        self.num_total_entries = 0
        self.num_total_entries_1D = 0
        self.num_total_entries_2D = 0
        for f in self.test_files:
            self.num_total_entries += self.count_mes(f, dimensions=-1)
            self.num_total_entries_1D += self.count_mes(f, dimensions=1)
            self.num_total_entries_2D += self.count_mes(f, dimensions=2)
            LumisectionHistogram1D.from_nanodqm(file_path=f)
            LumisectionHistogram2D.from_nanodqm(file_path=f)

    @skipIf(os.environ.get("GITHUB_WORKFLOW"), "Skipping nanoDQMIO tests on GitHub CI.")
    def test_nanodqmio_histogram_2d_parsing_resumption(self):
        """
        Try to partially read only 1 lumisection from a nanoDQMIO file.
        Verify the percentage processed and then read the remaining.
        """
        self._clear_db()

        test_file = self.test_files[0]

        num_entries = self.count_mes(test_file, dimensions=-1)
        num_entries_first_lumi = self.count_mes_first_lumi(test_file, dimensions=2)

        #num_lines = pd.read_csv(test_file).shape[0]
        #LumisectionHistogram2D.from_csv(file_path=test_file, read_chunk_num_max=1)
        LumisectionHistogram2D.from_nanodqm(file_path=test_file, read_chunk_lumi=1)

        test_file_db = HistogramDataFile.objects.get(filepath=test_file)
        assert math.isclose(
            test_file_db.percentage_processed,
            100 * (num_entries_first_lumi / num_entries),
            abs_tol=0.1,
        )

        # Read all the file
        LumisectionHistogram1D.from_nanodqm(file_path=test_file)
        LumisectionHistogram2D.from_nanodqm(file_path=test_file)
        test_file_db = HistogramDataFile.objects.get(filepath=test_file)
        logger.debug(f"{test_file_db.filepath}\t{test_file_db.entries_processed}\t{test_file_db.entries_total}\t{test_file_db.percentage_processed}")
        assert test_file_db.percentage_processed == 100.0

    @skipIf(os.environ.get("GITHUB_WORKFLOW"), "Skipping nanoDQMIO tests on GitHub CI.")
    def test_nanodqm_histogram_parsing_completeness(self):
        """
        Read all the available test files, and try to parse them into
        LumisectionHistogram1D and LumisectionHistogram2D entries. 
        Make sure they're parsed to completion.
        """
        self._clear_db()
        self._fillup_db()

        logger.debug(
            f"There are {LumisectionHistogram1D.objects.count()} "
            "1D Lumisection histograms in the DB"
        )
        logger.debug(
            f"There are {LumisectionHistogram2D.objects.count()} "
            "2D Lumisection histograms in the DB"
        )
        assert LumisectionHistogram1D.objects.count() == self.num_total_entries_1D
        assert LumisectionHistogram2D.objects.count() == self.num_total_entries_2D
        assert LumisectionHistogram1D.objects.count() + LumisectionHistogram2D.objects.count() == self.num_total_entries
        for hdf in HistogramDataFile.objects.all():
            logger.debug(f"{hdf.filepath}\t{hdf.entries_processed}\t{hdf.entries_total}\t{hdf.percentage_processed}")
            assert hdf.percentage_processed == 100.0

    @skipIf(os.environ.get("GITHUB_WORKFLOW"), "Skipping nanoDQMIO tests on GitHub CI.")
    def test_duplicate_entries(self):
        """
        Make sure that re-reading the same nanoDQMIO file will not lead to duplicate entries
        """
        self._clear_db()
        # Fillup db twice
        self._fillup_db()
        self._fillup_db()

        # Should not have changed
        assert LumisectionHistogram1D.objects.count() == self.num_total_entries_1D
        assert LumisectionHistogram2D.objects.count() == self.num_total_entries_2D
        assert LumisectionHistogram1D.objects.count() + LumisectionHistogram2D.objects.count() == self.num_total_entries

# TODO: Add test which partially stores a Histogram file, then tries to resume
# and verifies that it was added completely. Possible ways to do it:
# 1) Call the management command as a Thread, which will have to be killed
# somehow after some arbitrary time delay.
# 2) Call the management command as a subprocess. This requires that the venv
# is somehow activated first. Then, a SIGKILL should suffice.
# 3) Modify the from_file method to accept a limit to the lines it reads, so
# that the file is incompletely read.
