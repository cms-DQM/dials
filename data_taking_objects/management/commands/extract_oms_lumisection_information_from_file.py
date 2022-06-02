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

        # Create all runs in list_of_runs, ignore if already created
        Run.objects.bulk_create(
            [Run(run_number=run_number) for run_number in list_of_runs],
            ignore_conflicts=True,
        )

        logger.info(f"Creating Lumisections in bulk..")

        # Bulk create the objects
        Lumisection.objects.bulk_create(
            [
                Lumisection(
                    run=Run.objects.get(
                        run_number=row["run_number"],
                    ),
                    ls_number=row["lumisection_number"],
                )
                for index, row in df_rate[
                    ["run_number", "lumisection_number"]
                ].iterrows()
            ],
            ignore_conflicts=True,
            batch_size=1000,
        )

        # Prepare the queryset, select related objects and only keep required fields
        lumisections = (
            Lumisection.objects.filter(ls_number__in=df_rate["lumisection_number"])
            .select_related("run")
            .only("ls_number", "run")
        )

        logger.info(f"Updating Lumisections..")
        for lumisection in lumisections:
            # Add extra fields/values to update here
            try:
                lumisection.oms_zerobias_rate = df_rate.query(
                    "(lumisection_number == @lumisection.ls_number)&(run_number==@lumisection.run.run_number)"
                )["rate"].values[0]
            except IndexError:
                lumisection.oms_zerobias_rate = 0  # ???

        num_ls = Lumisection.objects.bulk_update(
            lumisections, ["oms_zerobias_rate"], batch_size=1000
        )

        logger.info(f"Updated {num_ls} lumisections")
