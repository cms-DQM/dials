import django_tables2 as tables
from run_histos.models import RunHisto

class RunHistoTable1D(tables.Table):
    run = tables.Column(accessor = 'run.run_number')
    primary_dataset = tables.Column(verbose_name = "Dataset")
    title = tables.Column()
    mean = tables.Column()
    rms = tables.Column(verbose_name = "RMS")
    skewness = tables.Column()
    kurtosis = tables.Column()

    class Meta:
        model = RunHisto
        fields = ()
        attrs = {"class": "table table-hover table-bordered"}

    