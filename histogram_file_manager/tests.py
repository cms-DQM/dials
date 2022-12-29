import os
from django.test import TestCase
from django.conf import settings


class HistogramDataFileTestCase(TestCase):
    def setUp(self):
        """
        Get the _choices list from the HistogramDataFileForm which
        will populate the default directory setup in the models (DIR_PATH_DQMIO_STORAGE).
        """
        self.all_files = []
        all_dirs = settings.DIR_PATH_DQMIO_STORAGE.split(":")

        for _ in all_dirs:
            for root, _, files in sorted(os.walk(dir)):
                for f in sorted(files):
                    self.all_files.append(os.path.join(root, f))

    def test_data_file_detection(self):
        """
        There should be at least one file in this directory when testing.
        """
        assert len(self.all_files) > 0
