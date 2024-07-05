import plotly.graph_objs as go
import plotly.offline as pyo

def volumeWeightedAveragePrice(n, askprice_df, asksize_df, bidprice_df, bidsize_df):
    cols = [f'{i}' for i in range(n)]
    vwap = ((askprice_df[cols]*asksize_df[cols]).sum(axis=1)-(bidprice_df[cols]*bidsize_df[cols]).sum(axis=1)) / (asksize_df[cols].sum(axis=1)-bidsize_df[cols].sum(axis=1))
    return vwap

def volumeWeightedSpread(n, askprice_df, asksize_df, bidprice_df, bidsize_df):
    cols = [f'{i}' for i in range(n)]
    vws = ((askprice_df[cols]*asksize_df[cols]).sum(axis=1)+(bidprice_df[cols]*bidsize_df[cols]).sum(axis=1))
    return vws

def volumeImbalance(n, asksize_df, bidsize_df):
    cols = [f'{i}' for i in range(n)]
    return asksize_df[cols].sum(axis=1)+bidsize_df[cols].sum(axis=1)

def feature_fig(askprice_df, asksize_df, bidprice_df, bidsize_df):
    ap = (askprice_df['0'] + bidprice_df['0']) / 2
    spread = askprice_df['0'] - bidprice_df['0']

    vwap10 = volumeWeightedAveragePrice(10, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vwap30 = volumeWeightedAveragePrice(30, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vwap60 = volumeWeightedAveragePrice(60, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vwap100 = volumeWeightedAveragePrice(100, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vws10 = volumeWeightedSpread(10, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vws30 = volumeWeightedSpread(30, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vws60 = volumeWeightedSpread(60, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vws100 = volumeWeightedSpread(100, askprice_df, asksize_df, bidprice_df, bidsize_df)
    vi10 = volumeImbalance(10, asksize_df, bidsize_df)
    vi30 = volumeImbalance(30, asksize_df, bidsize_df)
    vi60 = volumeImbalance(60, asksize_df, bidsize_df)
    vi100 = volumeImbalance(100, asksize_df, bidsize_df)

    fig_vwap = go.Figure()
    trace_1 = go.Scatter(x=vwap10.index, y=(vwap10-ap).values, mode='lines+markers', name='n=10')
    trace_2 = go.Scatter(x=vwap30.index, y=(vwap30-ap).values, mode='lines+markers', name='n=30')
    trace_3 = go.Scatter(x=vwap60.index, y=(vwap60-ap).values, mode='lines+markers', name='n=60')
    trace_4 = go.Scatter(x=vwap100.index, y=(vwap100-ap).values, mode='lines+markers', name='n=100')
    fig_vwap.add_trace(trace_1)
    fig_vwap.add_trace(trace_2)
    fig_vwap.add_trace(trace_3)
    fig_vwap.add_trace(trace_4)

    fig_vwap.update_layout(
        title='OBWAP-AP',
        xaxis_title='UNIX TIME',
        yaxis_title='OBWAP-AP',
        plot_bgcolor='white'
    )

    graph_vwap = pyo.plot(fig_vwap, output_type='div')

    fig_spread = go.Figure()
    trace_10 = go.Scatter(x=spread.index, y=spread.values, mode='lines+markers', name='spread')
    trace_11 = go.Scatter(x=vws10.index, y=vws10.values, mode='lines+markers', name='n=10')
    trace_12 = go.Scatter(x=vws30.index, y=vws30.values, mode='lines+markers', name='n=30')
    trace_13 = go.Scatter(x=vws60.index, y=vws60.values, mode='lines+markers', name='n=60')
    trace_14 = go.Scatter(x=vws100.index, y=vws100.values, mode='lines+markers', name='n=100')
    fig_spread.add_trace(trace_10)
    fig_spread.add_trace(trace_11)
    fig_spread.add_trace(trace_12)
    fig_spread.add_trace(trace_13)
    fig_spread.add_trace(trace_14)

    fig_spread.update_layout(
        title='OBWSpread and Spread',
        xaxis_title='UNIX TIME',
        yaxis_title='OBWS and S',
        plot_bgcolor='white'
    )

    graph_spread = pyo.plot(fig_vwap, output_type='div')

    fig_vi = go.Figure()
    trace_21 = go.Scatter(x=vi10.index, y=vi10.values, mode='lines+markers', name='n=10')
    trace_22 = go.Scatter(x=vi30.index, y=vi30.values, mode='lines+markers', name='n=30')
    trace_23 = go.Scatter(x=vi60.index, y=vi60.values, mode='lines+markers', name='n=60')
    trace_24 = go.Scatter(x=vi100.index, y=vi100.values, mode='lines+markers', name='n=100')
    fig_vi.add_trace(trace_21)
    fig_vi.add_trace(trace_22)
    fig_vi.add_trace(trace_23)
    fig_vi.add_trace(trace_24)

    fig_vi.update_layout(
        title='OrderBook Imbalance',
        xaxis_title='UNIX TIME',
        yaxis_title='OBI',
        plot_bgcolor='white'
    )

    graph_vi = pyo.plot(fig_vi, output_type='div')

    fig_ap = go.Figure()
    trace = go.Scatter(x=ap.index, y=ap.values, mode='lines+markers', name='AP')
    fig_ap.add_trace(trace)

    fig_ap.update_layout(
        title='Average Price',
        xaxis_title='UNIX TIME',
        yaxis_title='AP',
        plot_bgcolor='white'
    )

    graph_ap = pyo.plot(fig_ap, output_type='div')
    return graph_vwap, graph_spread, graph_vi, graph_ap

def scatter3d(askprice_df, asksize_df, bidprice_df, bidsize_df):
    points = []
    for idx in askprice_df.index:
        # jst = datetime.datetime.fromtimestamp(idx)+datetime.timedelta(hours=9)
        ask_points = [(idx-askprice_df.index[0], y, z) for y, z in zip(askprice_df.loc[idx].values, asksize_df.loc[idx].values)]
        points = points+ask_points
        bid_points = [(idx-askprice_df.index[0], y, z) for y, z in zip(bidprice_df.loc[idx].values, bidsize_df.loc[idx].values)]
        points = points + bid_points

    x_data = [item[0] for item in points]
    y_data = [item[1] for item in points]
    z_data = [item[2] for item in points]

    trace = go.Scatter3d(
        x=x_data,
        y=y_data,
        z=z_data,
        mode='markers',
        marker=dict(
            size=1,
            color='rgb(255, 0, 0)',    # 赤色
            opacity=0.8
        )
    )

    data = [trace]

    layout = go.Layout(
        title='orderbook history',
        scene=dict(
            xaxis=dict(title='日付', type='date'),
            # xaxis=dict(title='unixtime'),
            yaxis=dict(title='price'),
            zaxis=dict(title='size')
        )
    )

    fig = go.Figure(data=data, layout=layout)
    graph_ob = pyo.plot(fig, output_type='div')
    return graph_ob

