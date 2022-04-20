from math import remainder
from dash import Dash, html, dash_table, dcc, Output, Input
from plotly import express, graph_objects, subplots
import pandas
import sys
import os
import re

if len(sys.argv) == 2:
    MARKET = sys.argv[1]
else:
    print('Please input market as first input..')
    sys.exit()

INTERVAL = 60
defaultDirectory = f'data/{MARKET}'
defaultStock = sorted(os.listdir(f'{defaultDirectory}'))[0]
defaultFileName = sorted(os.listdir(f'{defaultDirectory}/{defaultStock}'))[-1]
FILENAME = f'{defaultDirectory}/{defaultStock}/{defaultFileName}' 
df = pandas.read_csv(FILENAME)

volume_df = df.loc[:, ['datetime', 'volume']]
volume_df.loc[:, 'datetime'] = df['datetime'].apply(lambda x: x.split()[1])

if __name__ == '__main__':

    def generateHtmlTables(df, interval):
        num = df.shape[0] // interval
        return [
            html.Div(children=[
                dash_table.DataTable(
                    id=f'table{i}',
                    style_cell={'textAlign': 'center'},
                    # style_cell={'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': '50px'},
                    style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
                    data=df.loc[i*interval:(i+1)*interval,].to_dict('records'),
                    columns=[{"name": col, "id": col} for col in df.columns]
                )
            ], style={'display': 'inline-block', 'width': f'{100//num}%'}) for i in range(num)
        ]

    app = Dash(__name__)

    img_candlestick = graph_objects.Figure(data=[graph_objects.Candlestick(
        x=df['datetime'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    img_candlestick.update_layout(xaxis_rangeslider_visible=False)
    img_volume = express.line(df, x='datetime', y='volume')

    if 1:
        app.layout = html.Div(children = [
            html.Div(children = [
                html.Div(children=[
                    html.Div(children="Stock Name", className="header-title"),
                    dcc.Dropdown(
                        id="stock-filter",
                        options=[
                            {"label": stock, "value": stock}
                            for stock in sorted(os.listdir(defaultDirectory))
                        ],
                        value=defaultStock,
                        clearable=False,
                        className='dropdown-1'
                    ),
                ]),
                html.Div(children=[
                    html.Div(children="Date", className="header-title"),
                    dcc.Dropdown(
                        id="date-filter",
                        # options=[{"label": defaultFileName, "value": defaultFileName}],
                        value=defaultFileName,
                        clearable=False,
                        className='dropdown'
                    ),
                ])
            # ], style={'display': 'flex', 'justify-content': 'space-evenly'}),
            ], className="menu"),
            html.Div(children = [
                dcc.Graph(id=f'img_1', figure=img_candlestick, style={'height': 750}),
                dcc.Graph(id=f'img_2', figure=img_volume, style={'height': 250})
            ]),
            *generateHtmlTables(volume_df, INTERVAL),
        ], style={'text-align': 'center'})
    else:
        app.layout = html.Div(children = [
            html.Div(children = [
                dash_table.DataTable(
                    id='table',
                    style_cell={'textAlign': 'center'},
                    # style_cell={'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': '50px'},
                    style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_size=4000 # default = 250
                )
            ])
        ])
        
    @app.callback(
        Output("date-filter", "options"), Input("stock-filter", "value")
    )
    def updateDateFilter(stock):
        return [{"label": date, "value": date} for date in sorted(os.listdir(f'{defaultDirectory}/{stock}'))]
        # return [{"label": date, "value": date} for date in sorted(os.listdir(f'{defaultDirectory}/{stock}'))]

    @app.callback(
        [Output("img_1", "figure"), Output("img_2", "figure")],
        [Input("stock-filter", "value"), Input("date-filter", "value")]
    )
    def updatePlot(stock, date):
        filePath = f'{defaultDirectory}/{stock}/{date}'
        df = pandas.read_csv(filePath)
        
        img_candlestick = graph_objects.Figure(data=[graph_objects.Candlestick(
            x=df['datetime'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )])
        img_candlestick.update_layout(xaxis_rangeslider_visible=False)
        img_volume = express.bar(df, x='datetime', y='volume')

        return img_candlestick, img_volume

    app.run_server(debug=True, host='0.0.0.0', port=8008)
