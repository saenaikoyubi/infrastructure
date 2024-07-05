from flask import Flask, render_template
import psycopg2
import plotly.graph_objs as go
import plotly.offline as pyo
import numpy as np
import pandas as pd

from fetcher import get_df, get_df_1min
from features import feature_fig, scatter3d

app = Flask(__name__)

@app.route('/')
def index():
    askprice_df, asksize_df, bidprice_df, bidsize_df = get_df_1min()
    # graph_ob = scatter3d(askprice_df=askprice_df, asksize_df=asksize_df, bidprice_df=bidprice_df, bidsize_df=bidsize_df)
    graph_vwap, graph_spread, graph_vi, graph_ap = feature_fig(askprice_df=askprice_df, asksize_df=asksize_df, bidprice_df=bidprice_df, bidsize_df=bidsize_df)

    return render_template('index.html', graph_vwap=graph_vwap, graph_spread=graph_spread, graph_vi=graph_vi, graph_ap=graph_ap)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
