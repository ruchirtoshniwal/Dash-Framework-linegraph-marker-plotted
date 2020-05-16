import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output


df_aapl_raw = pd.read_csv("data/AllianzCSV_CM.csv")


df_aapl_slice = df_aapl_raw[2:].reset_index()


df_aapl_slice['Year'] = pd.DatetimeIndex(df_aapl_slice['Date']).year


high1 = [-10.44, -25.28, -15.49]

Dates2 = ['01.02.2011', '02.02.2012', '03.02.2012']
low1 = [20.00, -1.36, -0.02]

app = dash.Dash(__name__)


app.layout = html.Div([
    
    html.Div([
        html.Div([
            
            html.Div([html.Div(dcc.RangeSlider(id="year selection", updatemode='drag',
                                               marks={i: '{}'.format(i) for i in df_aapl_slice.Year.unique().tolist()},
                                               min=df_aapl_slice.Year.min(), max=df_aapl_slice.Year.max(), value=[2010, 2012]),
                               className="row", style={"padding-bottom": 30,"width":"60%","margin":"auto"})
                      

                      ], className="row")
        ], className="six columns",style={"margin-right":0,"padding":0}),
        html.Div([
            dcc.Graph(id="plot-graph")
        ], className="six columns row",style={"margin-left":0,"padding":0}),
        
    ], className="row")
   ], className="container")






@app.callback(
    Output("plot-graph", 'figure'),
    [Input("year selection", 'value')])
def update_return(year):

    df_apl = df_aapl_slice[(df_aapl_slice["Year"] >= year[0]) & (df_aapl_slice["Year"] <= year[1])]
    

    stocks = pd.DataFrame({"Date": df_apl["Date"], "open": df_apl["OPENING"],
                           "close": df_apl["CLOSING"],"high": df_apl["HIGH"],"low": df_apl["LOW"],
                           "volume": df_apl["VOLUME"]})
    stocks = stocks.set_index('Date')
    stock_return = stocks.apply(lambda x: ((x - x[0]) / x[0])*100)

    trace2 = go.Scatter(x=df_apl['Date'], y=stock_return['open'], mode='lines', name='open')
    trace3 = go.Scatter(x=df_apl['Date'], y=stock_return['close'], mode='lines', name='close')
    trace4 = go.Scatter(x=['04.02.2010', '26.08.2011', '17.05.2012'], y=high1, marker=dict(size=12),
    mode='markers', name='Buy',text=["78.66", "64.38","74.2"],
    hovertemplate=
        
        "Date: %{x}<br>" +
        "close: %{y}<br>"+
        "High: <b>%{text}</b><br><br>" )
    trace5 = go.Scatter(x=['01.02.2011', '02.02.2012', '03.02.2012'], y=low1, marker=dict(color="crimson", size=12),
    mode='markers', name='Sale',text=["101.75", "85.86","86.65"],
    hovertemplate=
        "Date: %{x}<br>" +
        "close: %{y}<br>"+
        "High: <b>%{text}</b><br><br>" )
    layout2 = go.Layout({'title': 'Returns (%) : AAPL open vs AAPL close ',
                         "legend": {"orientation": "h","xanchor":"left"},
                         "xaxis": {
                             "rangeselector": {
                                 "buttons": [
                                     {"count": 6, "label": "6M", "step": "month",
                                      "stepmode": "backward"}
                                     
                                 ]
                             }}
                         })

    fig = {'data': [trace2,trace3,trace4,trace5],
           'layout': layout2
           }
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)