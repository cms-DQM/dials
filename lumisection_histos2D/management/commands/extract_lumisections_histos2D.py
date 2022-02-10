from django.core.management.base import BaseCommand

from runs.models import Run
from lumisections.models import Lumisection
from lumisection_histos2D.models import LumisectionHisto2D
import json

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
import pandas as pd


class Command(BaseCommand):
    help = "Extracts lumisection histos 2D from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        count = 0
        for df in pd.read_csv(file_path, chunksize=50):
            print(df.columns)
            
            lumisection_histos2D = []
            count2 = 0
            
            for index, row in df.iterrows():
                run_number = row["fromrun"]
                lumi_number = row["fromlumi"]
                title = row["hname"]
                entries = row["entries"]
                data=json.loads(row["histo"])

                print(run_number, lumi_number, title)

                run, _ = Run.objects.get_or_create(run_number=run_number)
                lumisection, _ = Lumisection.objects.get_or_create(run_number=run, ls_number=lumi_number)

                lumisection_histo2D = LumisectionHisto2D(
                    lumisection=lumisection,
                    title=title,
                    entries=entries,
                    data=data
                )

                lumisection_histos2D.append(lumisection_histo2D)
                count2 += 1
                if count2 == 10: 
                    LumisectionHisto2D.objects.bulk_create(lumisection_histos2D, ignore_conflicts=True)
                    print('10 2D lumisection histos 2D of chunk {} successfully added!'.format(count))
                    count2 = 0
                    lumisection_histos2D = []
                    #Add case for (less than 10 cases!)

            count +=1
