# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 23:30:28 2017

@author: rkprajap
"""
from bokeh.plotting import figure
from bokeh.io import push_notebook, show, output_notebook
from bokeh.models import DatetimeTickFormatter
import numpy as np
output_notebook()

# plotter
def SMA_plotter(code, df, x_axis_label):
    # create a new plot
    p = figure(title=code + " Simple Moving Averages", x_axis_label=x_axis_label, y_axis_label='Closing Price', width=800, x_axis_type='datetime')

    x_index = np.where(df.columns.values==x_axis_label)
    columns = np.delete(df.columns.values, x_index)
    print columns
    for item in columns:
        color = hex_code_color()
        if item == 'Close':
            p.line(df[x_axis_label], df[item], legend=item, line_color=color, line_width=3)
        else:
            p.line(df[x_axis_label], df[item], legend=item, line_color=color)
    
    p.xaxis.formatter=DatetimeTickFormatter(formats=dict(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    ))

    show(p, notebook_handle=True)
    
# calculate SMA scores from a given SMA list
def compute_SMA_scores(smalist, code, df):
    for sma in sma_list:
        df[str(sma)] = df['Close'].rolling(window=sma,center=False).mean()

    final_sma_values = df[[str(item) for item in smalist]].tail(1).values[0]
    sorted_sma = np.sort(sma_list)
    
    score = 0
    for index, sma in enumerate(sorted_sma):
        if df['Close'].values[0] < final_sma_values[index]:
            score = score + (index + 1)*sma
    temp_df = pd.DataFrame([[code, score]], columns=['Code', 'SMA_Score']).set_index(['Code'])
    return temp_df
