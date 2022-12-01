
import plotly.figure_factory as ff
import plotly.express as px
import pandas as pd


def displot(data:pd.DataFrame, labels):
    fig = ff.create_distplot(data, labels)
    return fig
