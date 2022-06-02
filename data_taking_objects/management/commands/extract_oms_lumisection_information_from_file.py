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
        logger.info(f"Found {len(list_of_runs)} runs")

        timestamp = time.time()

        # # Create all runs in list_of_runs, ignore if already created
        runs = Run.objects.bulk_create(
            [Run(run_number=run_number) for run_number in list_of_runs],
            ignore_conflicts=True,
        )
        print(
            f"Bulk create {len(runs)} runs took {time.time() - timestamp:.2f} seconds"
        )

        timestamp = time.time()

        # Run.objects.get() should not be raising DoesNotExist
        ls_objects = [
            Lumisection(
                run=Run.objects.get(
                    run_number=row["run_number"],
                ),
                ls_number=row["lumisection_number"],
            )
            for index, row in df_rate[["run_number", "lumisection_number"]].iterrows()
        ]
        print(
            f"Creation of {len(ls_objects)} ls entries took {time.time() - timestamp:.2f} seconds"
        )

        timestamp = time.time()
        l = Lumisection.objects.bulk_create(
            ls_objects,
            ignore_conflicts=True,
            batch_size=1000,
        )
        print(
            f"Bulk create {len(l)} lumisections took {time.time() - timestamp:.2f} seconds"
        )

        #######

        lumisections = (
            Lumisection.objects.filter(ls_number__in=df_rate["lumisection_number"])
            .select_related("run")
            .only("ls_number", "run")
        )
        #######

        # limit size for testing
        # lumisections = lumisections[:10000]

        timestamp = time.time()
        time_df = 0
        # Can't think of something smarter than this -- hits DB
        for lumisection in lumisections:
            try:
                timestamp_2 = time.time()
                rate = df_rate.query(
                    "(lumisection_number == @lumisection.ls_number)&(run_number==@lumisection.run.run_number)"
                )["rate"].values[0]
                time_df += time.time() - timestamp_2
                lumisection.oms_zerobias_rate = rate
            except IndexError:
                lumisection.oms_zerobias_rate = 0  # ???
        print(f"Time spent querying dataframe {time_df:.2f} seconds")
        print(
            f"Update {len(lumisections)} lumisections took {time.time() - timestamp:.2f} seconds"
        )

        timestamp = time.time()
        l = Lumisection.objects.bulk_update(
            lumisections, ["oms_zerobias_rate"], batch_size=10000
        )
        print(
            f"Bulk update {l} lumisections took {time.time() - timestamp:.2f} seconds"
        )
