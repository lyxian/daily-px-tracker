from dash import Dash, html, dash_table, dcc
from plotly import express, graph_objects, subplots
import pandas

FILENAME = 'data/C2PU.SI_1d_2022-04-05.csv'
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
                dcc.Graph(id=f'img_1', figure=img_candlestick, style={'height': 1500}),
                dcc.Graph(id=f'img_2', figure=img_volume, style={'height': 500})
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
        
    app.run_server(debug=True, host='0.0.0.0', port=8008)
