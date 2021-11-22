import pandas as pd
import altair as alt


def get_altair_chart(chart_type, *args, **kwargs):

    chart = {}

    df = kwargs.get('df')
 
    if chart_type == 'histogram':
        chart = alt.Chart(df).mark_bar().encode(
                    alt.X("mean", bin=True),
                    y='count()',
                ).to_json(indent=None)

    elif chart_type == 'time_serie':
        chart = alt.Chart(df).mark_circle(size=60).encode(
                    alt.X('run_number',
                        scale=alt.Scale(domain=(315000, 316000)) # shouldn't be hardcoded
                    ),
                    y='mean',
                    tooltip=['run_number', 'mean'],
                ).to_json(indent=None)

    else:
        print("No chart type was selected.")

    return chart 
