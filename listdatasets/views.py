from django.shortcuts import render
from listdatasets.models import Dataset
from tables.tables import DatasetTable


# Create your views here.
def listdatasets(request):
    """
    View to list all courses
    """
    context = {}

    lumi_list = Dataset.objects.all()
    lumi_table = DatasetTable(lumi_list)
    context["lumi_table"] = lumi_table

    run_list = Dataset.objects.all()
    run_table = DatasetTable(run_list)
    context["run_table"] = run_table

    fill_list = Dataset.objects.all()
    fill_table = DatasetTable(fill_list)
    context["fill_table"] = fill_table

    return render(request, "listdatasets/listdatasets.html", context)
