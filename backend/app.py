import subprocess
import requests
import json
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Output, Input, State


app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], assets_folder="assets")
app.title = "Trace Route"
app.layout = html.Div(
    style={"backgroundColor": "#303030", "height": "100vh"},
    children=[
        dbc.Container(
            style={"backgroundColor": "#303030","overflow":"hidden", "height": "100vh"},
            children=[
                html.H1("Ip Trace Route using Python and Map",
                        style={"color": "#fff", "textAlign": "center"}),
                html.P(id="user-ip-address",
                       style={"color": "#fff", "textAlign": "center"}),
                dbc.Input(id="ip-address", type="text",
                          placeholder="www.somewebsite.com or ip address"),
                html.Br(),
                dbc.Button('Trace', id="submit-value", n_clicks=0),
                html.Br(),
                html.Br(),
                dcc.Loading(
                    style={"backgroundColor": "#303030"},
                    id="loading-1",
                    type="default",
                    children=html.Div(
                        style={"width": "700px", "height": "100%"})

                ),

            ]
        )
    ]
)


def getLoc(IP):
    "Turn a string representing an IP address into a lat long pair"
    # Other geolocation services are available
    url = "https://geolocation-db.com/json/"+IP
    response = requests.get(url)
    data = json.loads(response.text)
    try:
        lat = float(data["latitude"])
        lon = float(data["longitude"])
        if lat == 0.0 and lon == 0.0:
            return (None, None)
        return (lat, lon)
    except:
        return (None, None)


@app.callback(
    [Output('loading-1', 'children'),
     Output('user-ip-address', 'children')],
    [Input('submit-value', 'n_clicks'),
     State('ip-address', 'value')]
)
def get_line(n_clicks, value):

    data = {
        'ip': [],
        'Latitude': [],
        'Longitude': [],

    }

    proc = subprocess.Popen(["traceroute -m 25 -n -4 "+value],
                            stdout=subprocess.PIPE, shell=True, universal_newlines=True)

    # Parse individual traceroute command lines
    for line in proc.stdout:
        print(line, end="")
        hopIP = line.split()[1]
        if hopIP in ("*", "to"):
            continue
        (lat, lon) = getLoc(hopIP)
        if (lat is None):
            continue
        if lon is None:
            continue
        data['ip'].append(hopIP)
        data['Latitude'].append(lat)
        data['Longitude'].append(lon)

    map_data = [
        {
            'type': 'scattergeo',
            'lat': data["Latitude"],
            'lon': data["Longitude"],
            'hoverinfo': 'none',
            'mode': 'lines',
            'line': {
                'width': 8,
                'color': '#707070'
            },
        },
        {
            'type': 'scattergeo',
            'lat': data["Latitude"],
            'lon': data["Longitude"],
            'hoverinfo': 'text+lon+lat',
            'text': 'Current Position',
            'mode': 'markers',
            'marker': {
                'size': 14,
                'color': '#ffe102'
            },
        }
    ]

    map_layout = {
        'geo': {
            'showframe': False,
            'showcoastlines': False,
            'showland': True,
            'showocean': True,
            'resolution': 100,
            'landcolor': '#303030',
            'oceancolor': '#0f0f0f',
            'scope': 'world',
            'showgrid': True,

        },
        'width': 1024,
        'height': 610,
        'showlegend': False,
        "paper_bgcolor": '#303030'

    }

    fig = {
        'data': map_data,
        'layout': map_layout
    }
    ip = subprocess.check_output(["myip"])
    return [dcc.Graph(id="show-map", config={
        'displayModeBar': False
    }, style={"backgroundColor": "#303030"}, figure=fig), "Your IP ADDRESS : {}".format(ip.decode("utf-8"))]


if __name__ == '__main__':
    app.run_server(debug=True)
