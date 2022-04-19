# https://betterprogramming.pub/3-techniques-for-importing-large-csv-files-into-a-django-app-2b6e5e47dba0
from django.core.management.base import BaseCommand
from data_taking_objects.models import Run


class Command(BaseCommand):
    help = "Add OMS information to the run"

    def get_oms_info(self):
        oms_fill = 0
        oms_lumisections = 0
        oms_initial_lumi = 0
        oms_end_lumi = 0

        oms_dict = {
            "oms_fill": oms_fill,
            "oms_lumisections": oms_lumisections,
            "oms_initial_lumi": oms_initial_lumi,
            "oms_end_lumi": oms_end_lumi,
        }

        return oms_dict

    def handle(self, *args, **options):

        run = 0

        oms_dict = self.get_oms_info(run)

        Run.objects.get_or_create(
            # run_number=run_number,
            oms_fill=oms_dict["oms_fill"],
            oms_lumisections=oms_dict["oms_lumisections"],
            oms_initial_lumi=oms_dict["oms_initial_lumi"],
            oms_end_lumi=oms_dict["oms_initial_lumi"],
        )
        # print(f'run {run_number} successfully added!')
