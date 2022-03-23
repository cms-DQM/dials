from django.core.management.base import BaseCommand

from histograms.models import LumisectionHistogram1D


class Command(BaseCommand):
    help = "Extracts lumisections histos 1D from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        LumisectionHistogram1D.from_csv(file_path)
