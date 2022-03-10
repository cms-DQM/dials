from rest_framework import routers
from histogram_file_manager.api.viewsets import HistogramDataFileViewset

router = routers.SimpleRouter()
router.register(r'histogram_data_files', HistogramDataFileViewset)
