# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0

import sys
import csv
import json
import random
import multiprocessing

from django.core.management import BaseCommand
from django.utils import timezone

from data_taking_objects.models import Run, Lumisection
from histograms.models import LumisectionHistogram2D

class Command(BaseCommand):
    help = "Loads 2D histograms for lumisections from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):

        print(f"Number of CPUs is {multiprocessing.cpu_count()}")

        csv.field_size_limit(100000000)

        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TrackerOfflineReferenceRuns
        list_of_runs = [323940, 321755, 321067, 318953, 317435, 317434, 316505, 316457, 315713, 315705, 315322, 315189, 314811, 314575]

        # https://mattermost.web.cern.ch/cms-exp/pl/64eeo77mpift9qzqyy5hdhefee
        list_of_mes = ["clusterposition_zphi_ontrack_PXLayer_1", 
                       "clusterposition_zphi_ontrack_PXLayer_2", 
                       "clusterposition_zphi_ontrack_PXLayer_3", 
                       "clusterposition_zphi_ontrack_PXLayer_4"] 

        # Generic implementation (to be optimized)
        start_time = timezone.now()

        file_path = options["file_path"]
        with open(file_path, "r") as csv_file:
            data = list(csv.reader(csv_file))
            lumisections = []
            lumisectionHistogram2Ds = []
            for row in data[1:]:
                print(row[2])
                if row[2] not in list_of_mes:
                    continue

                print(f"run {row[0]} / lumisection {row[1]} / histogram {row[2]}")
                run, _ = Run.objects.get_or_create(run_number=row[0])
                pk = 10000*int(row[0])+int(row[1])
                print(pk)

                lumisection = Lumisection(
                    run=run, 
                    ls_number=row[1],
                    pk=pk
                )
                lumisections.append(lumisection)

                lumisectionHistogram2D = LumisectionHistogram2D(
                    lumisection=lumisection,
                    title=row[2],
                    entries=row[8],
                    data=json.loads(row[7]),
                )
                lumisectionHistogram2Ds.append(lumisectionHistogram2D)

                if len(lumisections) > 500:
                    Lumisection.objects.bulk_create(lumisections, ignore_conflicts=True)
                    lumisections = []
                    print("Bulk created lumisections")
                    LumisectionHistogram2D.objects.bulk_create(lumisectionHistogram2Ds)
                    lumisectionHistogram2Ds = []
                    print("Bulk created histograms")


            print("Starting final bulk creation")
            print(f"{len(lumisections)} remaining histograms")
            Lumisection.objects.bulk_create(lumisections, ignore_conflicts=True)  
            print("Bulk created final lumisections")  
            LumisectionHistogram2D.objects.bulk_create(lumisectionHistogram2Ds)
            print("Bulk created final histograms")

        end_time = timezone.now()

        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
            )
        )
