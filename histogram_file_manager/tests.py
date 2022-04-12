import os
from django.test import TestCase
from django.conf import settings
from histogram_file_manager.models import HistogramDataFile


class HistogramDataFileTestCase(TestCase):

    def setUp(self):
        """
        Get the _choices list from the HistogramDataFileForm which
        will populate the default directory setup in the models (DIR_PATH_EOS_CMSML4DC).
        """
        self.all_files = []
        for root, dirs, files in sorted(os.walk(
                settings.DIR_PATH_EOS_CMSML4DC)):
            for f in sorted(files):
                self.all_files.append(os.path.join(root, f))

    def test_data_file_detection(self):
        """
        There should be at least one file in this directory when testing.
        """
        assert len(self.all_files) > 0
