from django.contrib import admin

# Register your models here.
from datasets.models import Dataset


admin.site.register(Dataset)