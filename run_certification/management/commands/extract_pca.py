from django.core.management.base import BaseCommand

from runs.models import Run
from run_histos.models import RunHisto
from run_certification.models import RunCertification

import pandas as pd


class Command(BaseCommand):
    help = 'Extracts PCA for each dataset using RunHisto'

    def handle(self, *args, **kwargs):
        runs_df      = pd.DataFrame(Run.objects.all().values())
        runhistos_df = pd.DataFrame(RunHisto.objects.all().values())

        if runhistos_df.shape[0] > 0:
            df = pd.merge(runs_df, runhistos_df, left_on='id', right_on='run_number_id').drop(['id_x', 'id_y', 'run_number_id', 'date_x', 'date_y'], axis=1)
            print(df.head(5))

        else:
	    print("No records in the database")
