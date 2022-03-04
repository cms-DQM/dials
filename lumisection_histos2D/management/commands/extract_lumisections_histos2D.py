from django.core.management.base import BaseCommand
from lumisection_histos2D.models import LumisectionHisto2D


class Command(BaseCommand):
    help = "Extracts lumisection histos 2D from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        LumisectionHisto2D.from_file(file_path)
