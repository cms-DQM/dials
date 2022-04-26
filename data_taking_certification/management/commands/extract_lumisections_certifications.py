from django.core.management.base import BaseCommand

from data_taking_objects.models import Run, Lumisection
from data_taking_certification.models import LumisectionCertification

import pandas as pd


class Command(BaseCommand):
    help = "Extracts certification for lumisections based on Run Registry files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        df_rr_lumisections = pd.read_pickle(file_path)

        print(df_rr_lumisections.head())
        print(df_rr_lumisections.columns.tolist())

        certifications = []

        for index, row in df_rr_lumisections[:200].iterrows():
            run_number = row["run_number"]

            run, _ = Run.objects.get_or_create(run_number=run_number)
            lumisection, _ = Lumisection.objects.get_or_create(
                run=run, ls_number=row["lumi_number"]
            )

            print(row)

            certification = LumisectionCertification(
                lumisection=lumisection,
                rr_is_golden_json=row["golden_flag"],
                rr_is_pixel_good=row["pixel_flag"],
                rr_is_strip_good=row["strip_flag"],
                rr_is_ecal_good=row["ecal_flag"],
                rr_is_hcal_good=row["hcal_flag"],
                rr_is_dt_good=row["dt_flag"],
                rr_is_csc_good=row["csc_flag"],
                rr_is_tracking_good=row["track_flag"],
                rr_is_muon_good=row["muon_flag"],
                rr_is_egamma_good=row["egamma_flag"],
                rr_is_jetmet_good=row["jetmet_flag"],
            )
            certifications.append(certification)

        LumisectionCertification.objects.bulk_create(certifications)

        print(f"{df_rr_lumisections.shape[0]} certifications successfully added!")
