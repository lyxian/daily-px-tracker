from dash import Dash, html, dash_table, dcc, Output, Input
from plotly import express, graph_objects, subplots
import pandas
import sys
import os

if len(sys.argv) == 2:
    MARKET = sys.argv[1]
else:
    print('Please input market as first input..')
    sys.exit()

defaultDirectory = f'data/{MARKET}'
defaultStock = os.listdir(f'{defaultDirectory}')[0]
defaultFileName = os.listdir(f'{defaultDirectory}/{defaultStock}')[0]
FILENAME = f'{defaultDirectory}/{defaultStock}/{defaultFileName}' 
df = pandas.read_csv(FILENAME)

if __name__ == '__main__':

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
                            for stock in os.listdir('data')
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
            ])
        ])
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
        [Output("date-filter", "options"), Output("date-filter", "value")],
        Input("stock-filter", "value")
    )
    def updateDateFilter(stock):
        return [{"label": date, "value": date} for date in os.listdir(f'{defaultDirectory}/{stock}')], os.listdir(f'{defaultDirectory}/{stock}')[0]

    @app.callback(
        [Output("img_1", "figure"), Output("img_2", "figure")],
        Input("date-filter", "value")
    )
    def updatePlot(file):
        filePath = f'{defaultDirectory}/{file.split("_")[0]}/{file}'
        df = pandas.read_csv(filePath)
        
        img_candlestick = graph_objects.Figure(data=[graph_objects.Candlestick(
            x=df['datetime'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )])
        img_candlestick.update_layout(xaxis_rangeslider_visible=False)
        img_volume = express.line(df, x='datetime', y='volume')

        return img_candlestick, img_volume

    app.run_server(debug=True, host='0.0.0.0', port=8008)
