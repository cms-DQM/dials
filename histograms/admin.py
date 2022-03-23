from django.contrib import admin
from histograms.models import RunHistogram, LumisectionHistogram1D, LumisectionHistogram2D

admin.site.register(RunHistogram)
admin.site.register(LumisectionHistogram1D)
admin.site.register(LumisectionHistogram2D)
