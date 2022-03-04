from django.core.management.base import BaseCommand

from lumisection_histos1D.models import LumisectionHisto1D


class Command(BaseCommand):
    help = "Extracts lumisections histos 1D from files"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        LumisectionHisto1D.from_file(file_path)
