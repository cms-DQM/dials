from django.core.management.base import BaseCommand

from data_taking_objects.models import Run
from data_taking_certification.models import RunCertification

import pandas as pd


class Command(BaseCommand):
    help = "Extracts certification for runs based on Run Registry file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        df_rr_run = pd.read_pickle(file_path)

        # print(df_rr_run.head())
        # print(df_rr_run.columns.tolist())

        cols = df_rr_run.columns[df_rr_run.dtypes.eq('float64')]
        print(cols)

        df_rr_run[cols] = df_rr_run[cols].apply(pd.to_numeric)
        print(df_rr_run.fraction_pixel_GOOD.dtypes)

        certifications = []

        for index, row in df_rr_run.iterrows():
            run, _ = Run.objects.get_or_create(run_number=row["run_number"])

            certification = RunCertification(
                run=run,
                rr_frac_pixel_good=row["fraction_pixel_GOOD"],
                rr_frac_strip_good=row["fraction_strip_GOOD"],
                rr_frac_ecal_good=row["fraction_ecal_GOOD"],
                rr_frac_hcal_good=row["fraction_hcal_GOOD"],
                rr_frac_dt_good=row["fraction_dt_GOOD"],
                rr_frac_csc_good=row["fraction_csc_GOOD"],
                rr_frac_tracking_good=row["fraction_track_GOOD"],
                rr_frac_muon_good=row["fraction_muon_GOOD"],
                rr_frac_egamma_good=row["fraction_egamma_GOOD"],
                rr_frac_tau_good=row["fraction_tau_GOOD"],
                rr_frac_jetmet_good=row["fraction_jetmet_GOOD"],
                rr_frac_btag_good=row["fraction_btag_GOOD"],
            )
            certifications.append(certification)

        RunCertification.objects.bulk_create(certifications)

        print(f"{df_rr_run.shape[0]} certifications successfully added!")
