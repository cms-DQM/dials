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

        # VERY VERY SLOW
        for index, row in df_rate.iterrows():

            run_number = row["attributes.run_number"]
            ls_number = row["attributes.first_lumisection_number"]
            rate = row["attributes.rate"]

            print(run_number, ls_number, rate)

            run, _ = Run.objects.get_or_create(run_number=run_number)
            lumisection, _ = Lumisection.objects.get_or_create(
                run=run, ls_number=ls_number, oms_zerobias_rate=rate
            )

            # alternatively
            # lumisection = Lumisection(...)
            # lumisections.append(lumisection)
            # Lumisection.objects.bulk_create(lumisections)
            # would require bulk_get_or_create...

            print(f"run {run_number} / ls {ls_number} rate successfully added!")
