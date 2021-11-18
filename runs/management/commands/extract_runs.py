from django.core.management.base import BaseCommand

from runs.models import Run

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
# dummy example since each file is actually only one run
import pandas as pd


class Command(BaseCommand):
    help = 'Extracts runs from files'

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        df = pd.read_csv(file_path)
        run_number = df.run.unique()[0]
        Run.objects.get_or_create(run_number=run_number)
        print(f'run {run_number} successfully added!')
