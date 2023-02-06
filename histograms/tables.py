import django_tables2 as tables
from django.utils.html import format_html
from histograms.models import (
    RunHistogram,
    LumisectionHistogram1D,
    LumisectionHistogram2D,
)


class RunHistogramTable(tables.Table):
    run = tables.Column(accessor="run.run_number")
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


class OneDimensionHistogramColumn(tables.Column):
    def render(self, record):
        return format_html("""
        <div id="histogram-{}" style="height: 100pt; width: 200pt;">
            <script>
                var data = [
                    {{
                        y: {},
                        type: 'bar'
                    }}
                ];

                Plotly.newPlot('histogram-{}', data, 
                {{margin: {{t: 10, b: 10, l: 10, r: 10}}, 
                yaxis: {{"visible": false}}, 
                xaxis: {{"visible": false}}, 
                bargap: 0, 
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
                }}, {{staticPlot: true}});
            </script>
        </div>
        """, record.id, record.data, record.id)

class TwoDimensionHistogramColumn(tables.Column):
    def render(self, record):
        return format_html("""
        <div id="histogram-{}" style="height: 100pt; width: 200pt;">
            <script>
                var data = [
                    {{
                        z: {},
                        type: 'heatmap',
                        colorscale: 'Viridis'
                    }}
                ];

                Plotly.newPlot('histogram-{}', data, 
                {{margin: {{t: 10, b: 10, l: 10, r: 10}}, 
                yaxis: {{"visible": false}}, 
                xaxis: {{"visible": false}}, 
                bargap: 0, 
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
                }}, {{staticPlot: true}});
            </script>
        </div>
        """, record.id, record.data, record.id)

class LumisectionHistogram1DTable(tables.Table):
    id = tables.Column()
    run = tables.Column(accessor="lumisection.run.run_number")
    lumisection = tables.Column(accessor="lumisection.ls_number")
    title = tables.Column(attrs={"td":{"style" : "min-width: 300px; word-break: break-all;" }})
    entries = tables.Column()
    data = OneDimensionHistogramColumn(verbose_name="Histogram Data")
    paginator_class = tables.LazyPaginator

    class Meta:
        model = LumisectionHistogram1D
        fields = ()
        attrs = {"class": "table table-hover table-striped"}


class LumisectionHistogram2DTable(tables.Table):
    id = tables.Column()
    run = tables.Column(accessor="lumisection.run.run_number")
    lumisection = tables.Column(accessor="lumisection.ls_number")
    title = tables.Column(attrs={"td":{"style" : "min-width: 300px; word-break: break-all;" }})
    entries = tables.Column()
    data = TwoDimensionHistogramColumn(verbose_name="Histogram Data")
    paginator_class = tables.LazyPaginator

    class Meta:
        model = LumisectionHistogram2D
        fields = ()
        attrs = {"class": "table table-hover table-striped"}
