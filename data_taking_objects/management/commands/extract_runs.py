from django.core.management.base import BaseCommand

from data_taking_objects.models import Run

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
# import pandas as pd


class Command(BaseCommand):
    help = "Extracts runs from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        split_file_path = file_path.replace(".csv", "").split("/")[-1].split("_")
        print(split_file_path)

        dataset = split_file_path[0]
        run_number = split_file_path[1]
        year = split_file_path[2][-4:]

        print(dataset, run_number, year)

        Run.objects.get_or_create(
            run_number=run_number,
            year=year,
        )
        print(f"run {run_number} successfully added!")
