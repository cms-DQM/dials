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

        name_mapping = {
            "attributes.run_number": "run_number",
            "attributes.first_lumisection_number": "lumisection_number",
            "attributes.rate": "rate",
        }

        df_rate = (
            df_rate[
                [
                    "attributes.run_number",
                    "attributes.first_lumisection_number",
                    "attributes.rate",
                ]
            ]
            .copy()
            .rename(columns=name_mapping)
        )

        list_of_runs = sorted(df_rate.run_number.unique())
        print(list_of_runs)

        for run_number in list_of_runs:

            run, _ = Run.objects.get_or_create(run_number=run_number)

            list_of_lumisections = sorted(
                df_rate.query("run_number==@run_number").lumisection_number.unique()
            )
            print(list_of_lumisections)

            lumisections_to_create_or_update = []

            for lumisection_number in list_of_lumisections:
                rate = df_rate.query(
                    "(run_number==@run_number)&(lumisection_number==@lumisection_number)"
                ).rate.values[0]

                print(f"Adding {run_number} / {lumisection_number} / {rate} to the DB")

                lumisection = Lumisection(
                    run=run, ls_number=lumisection_number, oms_zerobias_rate=rate
                )

                lumisections_to_create_or_update.append(lumisection)

            print("Trying bulk creation of objects")
            Lumisection.objects.bulk_create(
                lumisections_to_create_or_update, ignore_conflicts=True
            )

            print("Trying bulk update of objects")
            Lumisection.objects.bulk_update(
                lumisections_to_create_or_update, ["oms_zerobias_rate"]
            )
