import django_tables2 as tables
from lumisection_histos2D.models import LumisectionHisto2D

class LumisectionHistos2DTable(tables.Table):
    run = tables.Column(accessor = 'lumisection.run.run_number')
    lumisection = tables.Column(accessor = 'lumisection.ls_number')
    title = tables.Column()
    entries = tables.Column()
    data = tables.Column(verbose_name = "Histogram Data")

    class Meta:
        model = LumisectionHisto2D
        fields = ()
        attrs = {"class": "table table-hover table-bordered"}