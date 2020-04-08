# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Covid Plots
#
# I wanted to test out using jupyter notebook to show off some plotly graphs. So here goes.

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from covid_alberta import *


# %%
abC19scaper = albertaC19_webscraper.albertaC19_webscraper()
abTotal, abRegion, abTesting = abC19scaper.scrape_all(return_dataframes=True)


# %%
abTesting['total_tests'] = 0
abTesting['total_tests'] = abTesting.sum(axis=1)

region_cum = alberta_stats.calculate_cumulatives(abRegion, combine_df=True)
region_dt = alberta_stats.calculate_doublingtimes_region(region_cum, combine_df=False)
total_dt = alberta_stats.calculate_doublingtimes_region(abTotal, col_suffix='cum_cases', combine_df=False)

all_data = abTotal.join([total_dt, region_cum, region_dt, abTesting['total_tests']])
all_data.rename(columns={'new_cases': 'Ab_cases',
                         'cum_cases':'Ab_cumCases',
                         'dtime':'Ab_dtime',
                         'dtime_rw':'Ab_dtime_rw'}, inplace=True)


# %%
# Set up the defaults and the data
ln_width = 2
days_to_trim = 1
mode = 'lines'
trace_formats = {'Ab_cases': {'mode': mode,
                                 'line': {'color': 'green', 'width':ln_width},
                                 'name': 'Alberta Daily'},
                 'Calgary_cumCases': {'mode': mode,
                                      'line': {'color': 'orange', 'width':ln_width},
                                      'name': 'Calgary Cumulative'},
                 'Edmont_cumCases': {'mode': mode,
                                     'line': {'color': 'blue', 'width':ln_width},
                                     'name': 'Edmonton Cumulative'}
                }
plot_data = all_data[:-days_to_trim]
updated = plot_data.index[-1].strftime("%B %d")
# Create the plot
data = list()
date_fmt = "%m/%d"
for key in trace_formats.keys():
    data.append(go.Scatter(x=plot_data.index.strftime(date_fmt), y=plot_data[key],
                             mode=trace_formats[key]['mode'], line=trace_formats[key]['line'],
                             name=trace_formats[key]['name'],
                             )
                )
data.append(go.Bar(x=plot_data.index.strftime(date_fmt),  y=plot_data['total_tests'],
                     name='C19 Tests/day', yaxis='y2', marker={'color':'darkgrey'}))
layout = go.Layout(title=f'{updated} - Alberta Covid-19: Case Counts and Number of Tests',
                    xaxis=dict(domain=[0.01, 0.95], title='Date', titlefont={'size': 12},
                               rangemode='nonnegative', tick0=0, dtick=2, tickangle=45,
                               tickfont={'color':'black', 'size':10}),
                    yaxis=dict(title='Case Count', titlefont=dict(color='black'),
                               tickfont={'color':'black', 'size':11}, overlaying='y2', side='right',
                               rangemode='nonnegative', tick0=0, dtick=100),
                    yaxis2=dict(domain=[0.1, 0.95], title='New Tests per Day', titlefont={'size': 12, 'color':'black'},
                                tickfont={'color':'black', 'size':11}, showgrid=False,
                                anchor='x', side='left', rangemode='nonnegative', ticks='inside'),
                    legend_orientation="h", hovermode='x')
fig = go.Figure(data=data, layout=layout)
fig.show()
fig.write_html('images/Alberta_dailyCases.html')


# %%
# Set up the defaults and the data
ln_width = 2
days_to_trim = 1
mode = 'lines'
trace_formats = {'Alberta': {'x_data': 'Ab_cumCases',
                             'y_data': 'Ab_dtime_rw',
                             'mode': mode,
                             'line': {'color': 'green', 'width':ln_width}},
                 'Calgary': {'x_data': 'Calgary_cumCases',
                             'y_data': 'Calgary_dtime_rw',
                             'mode': mode,
                             'line': {'color': 'orange', 'width':ln_width}},
                 'Edmonton': {'x_data': 'Edmont_cumCases',
                              'y_data': 'Edmont_dtime_rw',
                              'mode': mode,
                              'line': {'color': 'blue', 'width':ln_width}}
                }
plot_data = all_data[:-days_to_trim]
updated = plot_data.index[-1].strftime("%B %d")
# Create the plot
fig = go.Figure()
annotations = list()
for key in trace_formats.keys():
    fig.add_trace(go.Scatter(x=plot_data[trace_formats[key]['x_data']], y=plot_data[trace_formats[key]['y_data']],
                             mode=trace_formats[key]['mode'], line=trace_formats[key]['line'],
                             name=key, hovertemplate='dt: %{y: 0.2f}'
                             ),
                 )
    last_x = plot_data[trace_formats[key]['x_data']][-1]
    last_y = plot_data[trace_formats[key]['y_data']][-1]
    last_day = plot_data.index[-1].strftime("%B %d")
    annotations.append(dict(x=last_x, y=last_y, xref='x', yref='y', text=last_day,
                            showarrow=True, ax=0, ay=-10))
fig.update_layout(dict(title=f'{updated} - Doubling Time: 6 day rolling window', titlefont={'size':20},
                        xaxis=dict(title='Cumulative Case Count', titlefont={'size': 10},
                                   rangemode='nonnegative', tick0=0, dtick=200,
                                   tickfont={'color':'black', 'size':10}),
                        yaxis=dict(title='Doubling Time (Days)', titlefont={'size': 10},
                                   tickfont={'color':'black', 'size':10}, side='left',
                                   rangemode='nonnegative', tick0=0, dtick=1),
                        legend_orientation="v", hovermode='x', annotations=annotations ))
fig.show()
fig.write_html('images/Alberta_doublingTime_RW.html')

