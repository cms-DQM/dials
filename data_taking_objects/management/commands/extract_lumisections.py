from django.core.management.base import BaseCommand

from data_taking_objects.models import Run, Lumisection

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
import pandas as pd


class Command(BaseCommand):
    help = "Extracts lumisections from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        df = pd.read_csv(file_path)

        lumisections = []

        for index, row in df.iterrows():
            run_number = row["fromrun"]
            lumi_number = row["fromlumi"]
            # print(run_number, lumi_number)

            run, _ = Run.objects.get_or_create(run_number=run_number)

            lumisection = Lumisection(
                run_number=run,
                ls_number=lumi_number,
            )

            lumisections.append(lumisection)

        Lumisection.objects.bulk_create(lumisections, ignore_conflicts=True)
        print('lumisections successfully added!')
