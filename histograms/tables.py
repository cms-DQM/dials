import django_tables2 as tables
from histograms.models import RunHistogram, LumisectionHistogram1D, LumisectionHistogram2D


class RunHistogramTable(tables.Table):
    run = tables.Column(accessor='run.run_number')
    primary_dataset = tables.Column(verbose_name="Dataset")
    title = tables.Column()
    entries = tables.Column()
    mean = tables.Column()
    rms = tables.Column(verbose_name="RMS")
    skewness = tables.Column()
    kurtosis = tables.Column()

    class Meta:
        model = RunHistogram
        fields = ()
        attrs = {"class": "table table-hover table-bordered"}


class LumisectionHistogram1DTable(tables.Table):
    run = tables.Column(accessor='lumisection.run.run_number')
    lumisection = tables.Column(accessor='lumisection.ls_number')
    title = tables.Column()
    entries = tables.Column()
    data = tables.Column(verbose_name="Histogram Data")

    class Meta:
        model = LumisectionHistogram1D
        fields = ()
        attrs = {"class": "table table-hover table-bordered"}


class LumisectionHistogram2DTable(tables.Table):
    run = tables.Column(accessor='lumisection.run.run_number')
    lumisection = tables.Column(accessor='lumisection.ls_number')
    title = tables.Column()
    entries = tables.Column()

    class Meta:
        model = LumisectionHistogram2D
        fields = ()
        attrs = {"class": "table table-hover table-bordered"}
