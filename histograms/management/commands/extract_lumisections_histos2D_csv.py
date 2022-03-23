from django.core.management.base import BaseCommand
from histograms.models import LumisectionHistogram2D


class Command(BaseCommand):
    help = "Extracts lumisection histos 2D from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        LumisectionHistogram2D.from_csv(file_path)
