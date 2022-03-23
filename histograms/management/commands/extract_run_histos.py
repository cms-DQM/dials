from django.core.management.base import BaseCommand

from runs.models import Run
from run_histos.models import RunHisto

# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
import pandas as pd


class Command(BaseCommand):
    help = 'Extracts histo summary from files'

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        split_file_path = file_path.replace('.csv', "").split('/')[-1].split('_')
        print(split_file_path)

        # opening per run file from ML4DQM
        df = pd.read_csv(file_path)

        # extracting and creating run number (ForeignKey of histo1DRun)
        dataset    = split_file_path[0]
        run_number = split_file_path[1]
        workspace  = 'TrackParameters/generalTracks/GeneralProperties'
        tag        = 'generalTracks'

        run, _ = Run.objects.get_or_create(run_number=run_number)
        print(f'run {run_number} successfully added!')

        # extracting set of histograms corresponding to the run
        dataset   = split_file_path[0]
        workspace = 'TrackParameters/generalTracks/GeneralProperties'
        tag       = 'generalTracks'

        df['subsystem'] = df['path'].map(lambda x: x.strip(';1').split('/')[2])
        print(df['subsystem'].unique())

        df['find_workspace'] = df['path'].apply(lambda x: True if workspace in x else False)
        df_workspace = df[df['find_workspace']]

        df_melt = df_workspace[['title', 'entries', 'mean', 'rms', 'skewness', 'kurtosis']]

        # creating instances of class Histo1DRun
        histos = []

        for index, row in df_melt.iterrows():
            #print(row['entries'], row['mean'], row['rms'])
            histo = RunHisto(
                run             = run,                      # would be better with Run.objects.get_or_create(run_number=run_number)
                primary_dataset = dataset,
                path            = workspace,
                title           = row['title'],
                entries         = row['entries'],
                mean            = row['mean'],
                rms             = row['rms'],
                skewness        = row['skewness'],
                kurtosis        = row['kurtosis'],
            )
            histos.append(histo)

        RunHisto.objects.bulk_create(histos)

        print(f'histograms from run {run_number} successfully added!')
