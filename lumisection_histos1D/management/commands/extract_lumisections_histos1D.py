from django.core.management.base import BaseCommand

from runs.models import Run
from lumisections.models import Lumisection
from lumisection_histos1D.models import LumisectionHisto1D
import json

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
import pandas as pd


class Command(BaseCommand):
    help = "Extracts lumisections histos 1D from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        df = pd.read_csv(file_path)
        print(df.head())
        print(df.columns)

        lumisection_histos1D = []
        count = 0

        for index, row in df.iterrows():
            run_number = row["fromrun"]
            lumi_number = row["fromlumi"]
            title = row["hname"]
            entries = row["entries"]
            data=json.loads(row["histo"])

            print(run_number, lumi_number, title)

            run, _ = Run.objects.get_or_create(run_number=run_number)
            lumisection, _ = Lumisection.objects.get_or_create(run=run, ls_number=lumi_number)

            lumisection_histo1D = LumisectionHisto1D(
                lumisection=lumisection,
                title=title,
                entries=entries,
                data=data
            )

            lumisection_histos1D.append(lumisection_histo1D)
            count += 1
            if count == 50:
                LumisectionHisto1D.objects.bulk_create(lumisection_histos1D, ignore_conflicts=True)
                print('50 lumisections 1D histograms successfully added!')
                count = 0
                lumisection_histos1D = []


