from django.contrib import admin

from .models import (
    Run,
    Lumisection,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)


admin.site.register(Run)
admin.site.register(Lumisection)
admin.site.register(LumisectionHistogram1D)
admin.site.register(LumisectionHistogram2D)
