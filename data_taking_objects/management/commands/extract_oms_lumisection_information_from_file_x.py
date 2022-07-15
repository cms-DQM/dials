import time
import logging
import pandas as pd
from django.core.management.base import BaseCommand
from data_taking_objects.models import Run, Lumisection

logger = logging.getLogger(__name__)


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
        logger.debug(f"Runs: {list_of_runs}")

        timestamp = time.time()

        num_runs = 0
        num_ls = 0
        time_create_runs = 0
        time_prepare_ls = 0
        time_create_ls = 0

        for run_number in list_of_runs:
            timestamp = time.time()
            run, _ = Run.objects.get_or_create(run_number=run_number)
            time_create_runs += time.time() - timestamp
            num_runs += 1

            timestamp = time.time()
            list_of_lumisections = sorted(
                df_rate.query("run_number==@run_number").lumisection_number.unique()
            )
            # logger.debug(f"Lumisections: {list_of_lumisections}")

            lumisections_to_create_or_update = []
            for lumisection_number in list_of_lumisections:
                rate = df_rate.query(
                    "(run_number==@run_number)&(lumisection_number==@lumisection_number)"
                ).rate.values[0]

                # logger.debug(
                #     f"Adding {run_number} / {lumisection_number} / {rate} to the DB"
                # )

                lumisection = Lumisection(
                    run=run, ls_number=lumisection_number, oms_zerobias_rate=rate
                )

                lumisections_to_create_or_update.append(lumisection)
            prepare_ls = time.time() - timestamp
            print(
                f"Preparation of {len(lumisections_to_create_or_update)} ls objects took {prepare_ls:.2f} seconds"
            )
            time_prepare_ls += prepare_ls

            timestamp = time.time()
            l = Lumisection.objects.bulk_create(
                lumisections_to_create_or_update, ignore_conflicts=True
            )
            time_ls = time.time() - timestamp
            print(f"Bulk create {len(l)} lumisections took {time_ls:.2f} seconds")
            time_create_ls += time_ls
            num_ls += len(l)

            # logger.debug("Trying bulk update of objects")
            # Lumisection.objects.bulk_update(
            #     lumisections_to_create_or_update, ["oms_zerobias_rate"]
            # )
        print(f"Creation of {num_runs} runs took {time_create_runs:.2f} seconds")
        print(
            f"Preparation of {num_ls} lumisections took {time_prepare_ls:.2f} seconds"
        )
        print(f"Bulk create {num_ls} lumisections took {time_create_ls:.2f} seconds")
