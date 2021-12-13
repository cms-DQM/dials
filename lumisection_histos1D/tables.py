import django_tables2 as tables
from lumisection_histos1D.models import LumisectionHisto1D

class LumisectionHistos1DTable(tables.Table):
    run = tables.Column(accessor = 'lumisection.run.run_number')
    lumisection = tables.Column(accessor = 'lumisection.ls_number')
    title = tables.Column()
    entries = tables.Column()
    data = tables.Column(verbose_name = "Hisrogram Data")

    class Meta:
        model = LumisectionHisto1D
        fields = ()
        attrs = {"class": "table table-hover table-bordered"}