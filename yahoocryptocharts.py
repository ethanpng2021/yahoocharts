import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas_datareader as pdr
import pandas as pd
import datetime, time
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
import subprocess
from subprocess import check_output
import pytz
from dateutil.relativedelta import *
#Data Source
import yfinance as yf



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
load_figure_template("vapor") ##https://pypi.org/project/dash-bootstrap-templates/
app.title = "Crypto and Stocks Viewer"

server = app.server


def get_datetime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
    hr = str(currentDT.time().hour)
    mi = str(currentDT.time().minute)
    sc = str(currentDT.time().second)
    ms = str(currentDT.time().microsecond)
    yr = int(currentDT.year)
    mth = int(currentDT.month)
    day = int(currentDT.day)
    timeString = hr+'_'+mi+'_'+sc+'_'+ms
    DATE = currentDT.strftime("%Y%m%d")
    DATE_UNDERSCORE = currentDT.strftime("%Y_%m_%d")
    markTime = hr + mi
    dateandtime = DATE + markTime
    return [yr, mth, day]

navbar = dbc.Navbar(
    [
        html.A(
       
            dbc.Row(
                [
                    
                    dbc.Col(dbc.NavbarBrand("Crypto & Stocks Viewer", className="ml-2"))
                    
                ],
                align="center",
          
            ),
            href="",
        ),

        
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            id="navbar-collapse", navbar=True, is_open=False
        ),
      
        
    ],
    color="dark",
    dark=True,
)





app.layout = dbc.Container([
            navbar,
    dbc.Row(
            [   
                dbc.Col(html.Div([

                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=[
                            {'label': 'BITCOIN (BTC-USD)', 'value': 'BTC-USD'},
                            {'label': 'ETHEREUM (ETH-USD)', 'value': 'ETH-USD'},
                            {'label': 'CARDANO (ADA-USD)', 'value': 'ADA-USD'},
                            {'label': 'BINANCECOIN (BNB-USD)', 'value': 'BNB-USD'},
                            {'label': 'XRP (XRP-USD)', 'value': 'XRP-USD'},
                            {'label': 'DOGECOIN (DOGE-USD)', 'value': 'DOGE-USD'},
                            {'label': 'SOLANA (SOL-USD)', 'value': 'SOL-USD'},
                            {'label': 'USDCOIN (USDC-USD)', 'value': 'USDC-USD'},
                            {'label': 'HEX (HEX-USD)', 'value': 'HEX-USD'},
                            {'label': 'POLKADOT (DOT-USD)', 'value': 'DOT-USD'},
                            {'label': 'UNISWAP (UNI-USD)', 'value': 'UNI-USD'},
                            {'label': 'BITCOINCASH (BCH-USD)', 'value': 'BCH-USD'},
                            {'label': 'LITECOIN (LTC-USD)', 'value': 'LTC-USD'},
                            {'label': 'CHAINLINK (LINK-USD)', 'value': 'LINK-USD'},
                            {'label': 'POLYGON (MATIC-USD)', 'value': 'MATIC-USD'},
                            {'label': 'STELLAR (XLM-USD)', 'value': 'XLM-USD'},
                            {'label': 'ETHEREUMCLASSIC (ETC-USD)', 'value': 'ETC-USD'},
                            {'label': 'INTERNETCOMPUTER (ICP-USD)', 'value': 'ICP-USD'},
                            {'label': 'VECHAIN (VET-USD)', 'value': 'VET-USD'},
                            {'label': 'THETA (THETA-USD)', 'value': 'THETA-USD'},
                            {'label': 'FILECOINFUTURES (FIL-USD)', 'value': 'FIL-USD'},
                            {'label': 'TRON (TRX-USD)', 'value': 'TRX-USD'},
                            {'label': 'AAVE (AAVE-USD)', 'value': 'AAVE-USD'},
                            {'label': 'Amazon.com, Inc.', 'value': 'AMZN'},
                            {'label': 'Tesla, Inc.', 'value': 'TSLA'},
                            {'label': 'Snap, Inc.', 'value': 'SNAP'},
                            {'label': 'Intel Comporation', 'value': 'INTC'},
                            {'label': 'Pinterest, Inc.', 'value': 'PINS'},
                            {'label': 'SoFi Technologies, Inc.', 'value': 'SOFI'},
                            {'label': 'Apple, Inc.', 'value': 'AAPL'},
                            {'label': 'New York Community Bancorp, Inc.', 'value': 'NYCB'},
                            {'label': 'Ford Motor Company', 'value': 'F'},
                            {'label': 'Advanced Micro Devices, Inc.', 'value': 'AMD'},
                            {'label': 'Bank of America Corporation', 'value': 'BAC'},
                            {'label': 'American Airlines Group Inc.', 'value': 'AAL'},
                            {'label': 'Southwestern Energy Company', 'value': 'SWN'},
                            {'label': 'AT&T Inc.', 'value': 'T'},
                            {'label': 'NIO, Inc.', 'value': 'NIO'},
                            {'label': 'Petróleo Brasileiro S.A. - Petrobras', 'value': 'PBR'},
                            {'label': 'Microsoft Corporation', 'value': 'MSFT'},
                            {'label': 'Meta Platforms, Inc.', 'value': 'META'},
                            {'label': 'Credit Suisse Group AG', 'value': 'CS'},
                            {'label': 'NVIDIA Corporation', 'value': 'NVDA'},
                            {'label': 'Alphabet Inc.', 'value': 'GOOGL'}
                        ],
                        value='BTC-USD',
                        clearable=False,
                        style={ #'width': '135px',
                                      'color': 'black',
                                      'background-color': 'aa2222',
                                      'fontSize': 16,
                                      'align-items': 'center',
                                      'justify-content': 'center',
                                    } 
                    ),
                

                    html.Hr(),

                    html.Div([
                    # calendar
                    html.P("From: "),
                    dcc.DatePickerSingle(
                        id='fromdate',
                        #min_date_allowed=date(1995, 8, 5),
                        #max_date_allowed=date(2017, 9, 19),
                        #initial_visible_month=date(2017, 8, 5),
                        date=datetime.date(2022, 4, 1)
                       
                    )], style={'align-items':"center", 'justify-content':"center"}),

                    html.Br(),

                    html.Div([
                    html.P("To: "),
                    dcc.DatePickerSingle(
                        id='todate',
                        #min_date_allowed=date(1995, 8, 5),
                        #max_date_allowed=date(2017, 9, 19),
                        #initial_visible_month=date(2017, 8, 5),
                        date=datetime.date.today()
                    )], style={'align-items':"center", 'justify-content':"center"})


                    ]), width=2),
               
                dbc.Col(html.Div([
                    dcc.Graph(id="graph"),
    
                    ]), width=9),
                
                
            ]
        ),

        

], fluid=True)



@app.callback(
    Output("graph", "figure"), 
    [Input("demo-dropdown", "value"),
     Input("fromdate", "date"),
     Input("todate", "date")])
def display_candlestick(value, fromdate, todate):

    if not value:
        value = "BTC-USD"

    if fromdate is None:
        date = datetime.datetime.now()
        d = date + relativedelta(months=-6)
        fromdate = datetime.date(d.year, d.month, d.day)
        fromdate = fromdate.strftime('%Y-%m-%d')

    if todate is None:
        d = get_datetime()
        todate = datetime.date(d[0], d[1], d[2])
        todate = todate.strftime('%Y-%m-%d')
        

    flist = fromdate.split('-')
    tlist = todate.split('-')
    from_yr = int(flist[0])
    from_mth = int(flist[1])
    from_day = int(flist[2])
    to_yr = int(tlist[0])
    to_mth = int(tlist[1])
    to_day = int(tlist[2])
    start = datetime.datetime(from_yr,from_mth,from_day)
    end = datetime.datetime(to_yr,to_mth,to_day)

    df = yf.download(value, start = start, end=end)

    SMA5  = df['Close'].rolling(5).mean()
    SMA10 = df['Close'].rolling(10).mean()
    SMA20 = df['Close'].rolling(20).mean()
    SMA30 = df['Close'].rolling(30).mean()
    SMA50 = df['Close'].rolling(50).mean()
    SMA60 = df['Close'].rolling(60).mean()
    SMA100 = df['Close'].rolling(100).mean()
    SMA200 = df['Close'].rolling(200).mean()
    
    data = [go.Candlestick(x=df.index,
                           open=df.Open,
                           high=df.High,
                           low=df.Low,
                           close=df.Close,
                           name='K')]

    s5 = go.Scatter(x = SMA5.index,y = SMA5.values,name = '5MA')
    s10 = go.Scatter(x = SMA10.index,y = SMA10.values,name = '10MA')
    s20 = go.Scatter(x = SMA20.index,y = SMA20.values,name = '20MA')
    s30 = go.Scatter(x = SMA30.index,y = SMA30.values,name = '30MA')
    s50 = go.Scatter(x = SMA50.index,y = SMA50.values,name = '50MA')
    s60 = go.Scatter(x = SMA60.index,y = SMA60.values,name = '60MA')
    s100 = go.Scatter(x = SMA100.index,y = SMA100.values,name = '100MA')
    s200 = go.Scatter(x = SMA200.index,y = SMA200.values,name = '200MA')
    
    layout = go.Layout(
                      title=value,
                      height=680,
                      #width=640,
                      xaxis={'rangeslider':{'visible':False}},

                      )             

    fig = go.Figure(data=data,layout=layout)

    fig.add_trace(s5)
    fig.add_trace(s10)
    fig.add_trace(s20)
    fig.add_trace(s30)
    fig.add_trace(s50)
    fig.add_trace(s60)
    fig.add_trace(s100)
    fig.add_trace(s200)
    
    return fig



if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(host="0.0.0.0", debug=True, dev_tools_ui=False, dev_tools_props_check=False, use_reloader=False)
