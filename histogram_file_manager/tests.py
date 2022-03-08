from django.test import TestCase
from django.conf import settings
from histogram_file_manager.forms import HistogramDataFileForm
from histogram_file_manager.modeils import HistogramDataFile


class HistogramDataFileTestCase(TestCase):
    def setUp(self):
        """
        Get the _choices list from the HistogramDataFileForm which
        will populate the default directory setup in the models (DIR_PATH_EOS_CMSML4DC).
        """
        self.all_files = [
            f[0]
            for f in HistogramDataFileForm().fields.get('filepath')._choices
        ]

    def test_data_file_detection(self):
        """
        There should be at least one file in this directory when testing.
        """
        assert len(self.all_files) > 0
