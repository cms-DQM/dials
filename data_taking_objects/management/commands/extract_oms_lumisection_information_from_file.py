# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
from django.core.management.base import BaseCommand
from data_taking_objects.models import Run, Lumisection

import pandas as pd

class Command(BaseCommand):
    help = "Add OMS information to the run"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def get_oms_info(self):
        return

    def handle(self, *args, **options):

        file_path = options["file_path"]

        df_rate = pd.read_pickle(file_path)

        print(df_rate.head())

        # run, _ = Run.objects.get_or_create(run_number=run_number)
        # lumisection, _ = Lumisection.objects.get_or_create(run=run)

        # print(f'run {run_number} successfully added!')
