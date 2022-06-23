import dash
import csv
import os
import base64
from PIL import Image
import matplotlib
from matplotlib import cm
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import dash_bootstrap_components as dbc
from collections import OrderedDict
import visdcc

resolution = 10000											#change resolution
chromosome = 4												#change chromosome number
available_normalizations = []
initial_check_boxes = []
job_path = 'job_tadmaster'								# change output_path 
heat_matrix_path = job_path + '/normalizations'
for directory in os.listdir(job_path + '/output/'):
    if not directory.startswith('.'):
        available_normalizations.append(os.path.join(job_path + '/output/', directory))
available_options = [{'label': os.path.basename(i), 'value': i} for i in available_normalizations]
default_normalization = available_normalizations[0]
current_directory = default_normalization
for file in os.listdir(current_directory):
    initial_check_boxes.append(file)
initial_drop_down = initial_check_boxes[0]
color_scales = list(set(plt.colormaps()).intersection(px.colors.named_colorscales()))
color_scales.append('TadMaster')
colors = ["Aqua", "Blue", "Chartreuse", "Gold", "DeepPink", "DarkViolet",
          "Gray", "Brown", "DarkGreen", "Orchid", "Olive", "Tan", "Yellow",
          "Khaki", "DarkBlue", "Crimson", "SandyBrown", "Violet", "PowderBlue"]
tad_master_color = [[0.0, "rgb(255,255,255)"],
                    [0.1111111111111111, "rgb(255,230,230)"],
                    [0.2222222222222222, "rgb(255,153,153)"],
                    [0.3333333333333333, "rgb(255,77,77)"],
                    [0.4444444444444444, "rgb(255,0,0)"],
                    [0.5555555555555556, "rgb(255,42,0)"],
                    [0.6666666666666666, "rgb(255,85,0)"],
                    [0.7777777777777778, "rgb(255,173,0)"],
                    [0.8888888888888888, "rgb(255,213,0)"],
                    [1.0, "rgb(255,255,0)"]]



# ------------------------------------------------------------------------------

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

# ------------------------------------------------------------------------------

app.layout = html.Div([
    dcc.Store(id='TAD dict'),
    dcc.Store(id='TAD dict binned'),
    dcc.Store(id='Color dict'),
    dcc.Store(id='MoC data'),
    visdcc.Run_js('javascript'),
    html.Div(
        [
            dbc.Row(
                dbc.Col(
                    style = {"marginTop": "100px", "backgroundColor": "#f2f2f2", "paddingTop": "25px", "paddingBottom": "15px", "borderRadius": "10px"},
                    children = html.Div([

    # ------------------------------------------------------------------------------
    # Normalizations
    # ------------------------------------------------------------------------------

    html.Div([
        html.H2(children="Select Normalization", className="header_text", 
                style={"textAlign": "center", "color": "#708090", "fontWeight": "600"}),
        # html.Div(children="Select Normalization",
        #          style={"font-size": "200%", "color": "black"}),



        dbc.FormGroup(
            [
                dbc.RadioItems(
                    options=[{'label': os.path.basename(i), 'value': i} for i in available_normalizations],
                    value=default_normalization,
                    id="Normalization",
                    inline=True,
                ),
            ]
        ),

    ], style={"text-align": "center"}),
    # ------------------------------------------------------------------------------
    # Number of TADs
    # ------------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="Number of TADs", className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-number tad",
                                size='lg',
                                color="light",
                                block=True,
                            ),
                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Select Methods:", style={"marginTop": "10px"}),
                                                            dbc.Checklist(
                                                                id="Number TADs Options",
                                                                inline=True,
                                                                style={"textAlign": "center"}
                                                            ),
                                                            dbc.Label("Plot Width Slider", html_for="slider"),
                                                            dcc.Slider(id='num-TAD-slider', min=5, max=100, step=5,
                                                                       value=50, ),
                                                        ]

                                                    ),
                                                    width={"size": 10, "offset": 1},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-j",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="Number TADs Plot", style={}), ],
                                                                    style={'display': 'flex', 'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-number tad",
                                is_open=True
                            )
                        ], style={'marginTop': 20}),
    # ------------------------------------------------------------------------------
    # Size of TADs
    # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="Size of TADs", className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-size tad",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Select Methods:", style={"marginTop": "10px"}),
                                                            dbc.Checklist(
                                                                id="Whisker Options",
                                                                inline=True,
                                                                style={"textAlign": "center"}
                                                            ),
                                                            dbc.Label("Plot Width Slider", html_for="slider"),
                                                            dcc.Slider(id='size-TAD-slider', min=5, max=100, step=5,
                                                                       value=50, ),

                                                        ]
                                                    ),
                                                    width={"size": 10, "offset": 1},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-a",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="Whisker Plot", style={}), ],
                                                                    style={'display': 'flex', 'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-size tad",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),
                        # ------------------------------------------------------------------------------
                        # Shared Boundaries
                        # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="Number of Shared Boundaries", className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-shared bound",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Select Methods:", style={"marginTop": "10px"}),
                                                            dbc.RadioItems(
                                                                id="Boundary Options",
                                                                inline=True,
                                                                style={"textAlign": "center"}
                                                            ),
                                                            dbc.Label("Plot Width Slider", html_for="slider"),
                                                            dcc.Slider(id='shared-boundaries-slider', min=5, max=100,
                                                                       step=5, value=100, ),

                                                        ]
                                                    ),
                                                    width={"size": 10, "offset": 1},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-b",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="Boundary Plot", style={}), ],
                                                                    style={'display': 'flex', 'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-shared bound",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),
                        # ------------------------------------------------------------------------------
                        # Stacked Boundaries
                        # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="Stacked Shared Boundaries", className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-stacked bound",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Select Tolerance (genomic bins):",
                                                                      style={"marginTop": "10px"}),
                                                            dbc.RadioItems(
                                                                id="Stacked Boundary Options",
                                                                options=[{'label': 'Zero', 'value': '0'},
                                                                         {'label': 'One', 'value': '1'},
                                                                         {'label': 'Two', 'value': '2'},
                                                                         {'label': 'Three', 'value': '3'}],
                                                                value='1',
                                                                inline=True,
                                                                style={"textAlign": "center"}
                                                            ),
                                                            dbc.Label("Plot Width Slider", html_for="slider"),
                                                            dcc.Slider(id='stacked-boundary-slider', min=5, max=100,
                                                                       step=5, value=50, ),

                                                        ],
                                                    ),
                                                    width={"size": 10, "offset": 1},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-c",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="Stacked Boundary Plot", style={}), ],
                                                                    style={'display': 'flex', 'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-stacked bound",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),
                        # ------------------------------------------------------------------------------
                        # Stacked Domains
                        # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="Stacked Shared Domains", className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-stacked domain",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Select Tolerance (genomic bins):",
                                                                      style={"marginTop": "10px"}),
                                                            dbc.RadioItems(
                                                                id="Stacked Domain Options",
                                                                options=[{'label': 'Zero', 'value': '0'},
                                                                         {'label': 'One', 'value': '1'},
                                                                         {'label': 'Two', 'value': '2'},
                                                                         {'label': 'Three', 'value': '3'}],
                                                                value='1',
                                                                inline=True,
                                                                style={"textAlign": "center"}
                                                            ),
                                                            dbc.Label("Plot Width Slider", html_for="slider"),
                                                            dcc.Slider(id='stacked-domain-slider', min=5, max=100,
                                                                       step=5, value=50, ),

                                                        ]
                                                    ),
                                                    width={"size": 10, "offset": 1},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-d",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="Stacked Domain Plot", style={}), ],
                                                                    style={'width': '100%', 'display': 'flex',
                                                                           'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-stacked domain",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),
                        # ------------------------------------------------------------------------------
                        # MoC Compare
                        # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="Comparison of Domain Overlap (Measure of Concordance)",
                                        className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-MoC compare",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Select Method:", style={"marginTop": "10px"}),
                                                            dbc.RadioItems(
                                                                id="MoC Options",
                                                                inline=True,
                                                                style={"textAlign": "center"}
                                                            ),
                                                            dbc.Label("Plot Width Slider", html_for="slider"),
                                                            dcc.Slider(id='moc-compare-slider', min=5, max=100, step=5,
                                                                       value=50, ),

                                                        ]
                                                    ),
                                                    width={"size": 10, "offset": 1},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-e",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="MoC Comparison Plot", style={}), ],
                                                                    style={'width': '100%', 'display': 'flex',
                                                                           'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-MoC compare",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),
                        # ------------------------------------------------------------------------------
                        # MoC Average
                        # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="Comparison of Average Domain Overlap (Measure of Concordance)",
                                        className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-MoC average",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Plot Width Slider", style={"marginTop": "10px"}),
                                                            dcc.Slider(id='moc-average-slider', min=5, max=100, step=5,
                                                                       value=50, ),
                                                        ]
                                                    ),
                                                    width={"size": 10, "offset": 1},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-f",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="MoC Plot", style={}), ],
                                                                    style={'width': '100%', 'display': 'flex',
                                                                           'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",

                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-MoC average",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),
                        # ------------------------------------------------------------------------------
                        # TNSE
                        # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="TSNE Comparison", className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-TSNE",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Select Perplexity:",
                                                                      style={"marginTop": "10px"}),
                                                            dcc.Slider(id='TSNE Slider',
                                                                       min=1,
                                                                       max=15,
                                                                       step=1,
                                                                       marks={1: '1',
                                                                              3: '3',
                                                                              5: '5',
                                                                              7: '7',
                                                                              9: '9',
                                                                              11: '11',
                                                                              13: '13',
                                                                              15: '15'},
                                                                       value=3,
                                                                       className="text-center"
                                                                       ),
                                                            dbc.Label("Marker Size Slider", html_for="slider"),
                                                            dcc.Slider(id='tnse-marker-slider', min=1, max=20, step=1,
                                                                       value=10, ),
                                                        ], style={'width': '100%', 'display': 'inline-block'}
                                                    ),
                                                    width={"size": 6, "offset": 3},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-g",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="TSNE Plot", style={'width': '100%',
                                                                                                     'height': '100%'}), ],
                                                                    style={'width': '100%', 'height': '100%',
                                                                           'display': 'flex', 'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                                style={'height': '63vw'})
                                                        ], style={'height': '63vw'})]),

                                ],

                                id="collapse-TSNE",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),
                        # ------------------------------------------------------------------------------
                        # PCA
                        # -----------------------------------------------------------------------------
                        html.Div([
                            dbc.Button(
                                html.H4(children="PCA Comparison", className="header_text",
                                        style={"textAlign": "center", "fontWeight": "600", "marginBottom": "0px"}),
                                id="collapse-button-PCA",
                                size='lg',
                                color="light",
                                block=True,
                            ),

                            dbc.Collapse(
                                [
                                    html.Div(
                                        [
                                            dbc.Row(
                                                dbc.Col(

                                                    children=dbc.FormGroup(
                                                        [
                                                            dbc.Label("Marker Size Slider",
                                                                      style={"marginTop": "10px"}),
                                                            dcc.Slider(id='pca-marker-slider', min=1, max=20, step=1,
                                                                       value=10, ),
                                                        ], style={'width': '100%', 'display': 'inline-block'}
                                                    ),
                                                    width={"size": 6, "offset": 3},
                                                )
                                            ),
                                        ]
                                    ),

                                    html.Hr(),
                                    dcc.Loading(id="loading-icon-h",
                                                children=[
                                                    html.Div(
                                                        [
                                                            dbc.Card(
                                                                dbc.CardBody(children=html.Div([
                                                                    dcc.Graph(id="PCA Plot", style={'width': '100%',
                                                                                                    'height': '100%'}), ],
                                                                    style={'width': '100%', 'display': 'flex',
                                                                           'align-items': 'center',
                                                                           'justify-content': 'center'})),
                                                                className="mb-3",
                                                            )
                                                        ]
                                                    )])

                                ],

                                id="collapse-PCA",
                                is_open=True
                            )

                        ], style={'marginTop': 20}),

                    ]),

                    width={"size": 8, "offset": 2},
                )
            ),
        ]
    )
])


# ------------------------------------------------------------------------------
# Collapse Callbacks
# -----------------------------------------------------------------------------
@app.callback(
    Output("collapse-number tad", "is_open"),
    Input("collapse-button-number tad", "n_clicks"),
    State("collapse-number tad", "is_open"),
)
def toggle_collapse_number_tad(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-size tad", "is_open"),
    Input("collapse-button-size tad", "n_clicks"),
    State("collapse-size tad", "is_open"),
)
def toggle_collapse_size_tad(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-shared bound", "is_open"),
    Input("collapse-button-shared bound", "n_clicks"),
    State("collapse-shared bound", "is_open"),
)
def toggle_collapse_shared_bound(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-stacked bound", "is_open"),
    Input("collapse-button-stacked bound", "n_clicks"),
    State("collapse-stacked bound", "is_open"),
)
def toggle_collapse_stacked_bound(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-stacked domain", "is_open"),
    Input("collapse-button-stacked domain", "n_clicks"),
    State("collapse-stacked domain", "is_open"),
)
def toggle_collapse_stacked_domain(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-MoC compare", "is_open"),
    Input("collapse-button-MoC compare", "n_clicks"),
    State("collapse-MoC compare", "is_open"),
)
def toggle_collapse_moc_compare(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-MoC average", "is_open"),
    Input("collapse-button-MoC average", "n_clicks"),
    State("collapse-MoC average", "is_open"),
)
def toggle_collapse_moc_average(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-TSNE", "is_open"),
    Input("collapse-button-TSNE", "n_clicks"),
    State("collapse-TSNE", "is_open"),
)
def toggle_collapse_tsne(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-PCA", "is_open"),
    Input("collapse-button-PCA", "n_clicks"),
    State("collapse-PCA", "is_open"),
)
def toggle_collapse_pca(n, is_open):
    if n:
        return not is_open
    return is_open
# ------------------------------------------------------------------------------
# Dynamic Option Callbacks
# -----------------------------------------------------------------------------



@app.callback(
    [Output('Number TADs Options', 'options'),
     Output('Whisker Options', 'options'),
     Output('Boundary Options', 'options'),
     Output('MoC Options', 'options')],
     Input('Normalization', 'value'))
def set_options(norm_path):
    options = []
    for filename in os.listdir(norm_path):
        if not filename.startswith('.') and os.stat(os.path.join(norm_path, filename)).st_size != 0 and "Zone.Identifier" not in str(os.path.basename(filename)):
            with open(os.path.join(norm_path, filename), 'r') as file:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(file.read(1024))
                file.seek(0)
                tad_data = [[digit for digit in line.strip().split(sep=dialect.delimiter)] for line in file]
                if len(tad_data[0]) == 2:
                    tad_data = np.asarray(tad_data, dtype='float')
                elif len(tad_data[0]) == 3:
                    temp_data = []
                    for i in range(len(tad_data)):
                        if tad_data[i][0] == str(chromosome) or tad_data[i][0] == 'chr' + str(chromosome):
                            temp_data.append(tad_data[i][1:])
                    tad_data = np.asarray(temp_data, dtype='float')
                if tad_data.size != 0:
                    options.append({'label': filename[:-4], 'value': filename})
    return [options, options, options, options]



@app.callback(
    Output('Number TADs Options', 'value'),
    Input('Number TADs Options', 'options'))
def set_num_tads_value(available_options):
    return [available_options[0]['value']]


@app.callback(
    Output('Whisker Options', 'value'),
    Input('Whisker Options', 'options'))
def set_whisker_value(available_options):
    return [available_options[0]['value']]


@app.callback(
    Output('Boundary Options', 'value'),
    Input('Boundary Options', 'options'))
def set_boundary_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('MoC Options', 'value'),
    Input('MoC Options', 'options'))
def set_MoC_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('Number TADs Plot', 'style'),
    [Input('num-TAD-slider', 'value')])
def set_num_tads_options(size):
    style = {}
    style['width'] = str(size) + '%'
    style['height'] = str(size) + '%'
    return style


@app.callback(
    Output('Whisker Plot', 'style'),
    [Input('size-TAD-slider', 'value')])
def set_num_tads_options(size):
    style = {}
    style['width'] = str(size) + '%'
    style['height'] = str(size) + '%'
    return style


@app.callback(
    Output('Boundary Plot', 'style'),
    [Input('shared-boundaries-slider', 'value')])
def set_num_tads_options(size):
    style = {}
    style['width'] = str(size) + '%'
    style['height'] = str(size) + '%'
    return style


@app.callback(
    Output('Stacked Boundary Plot', 'style'),
    [Input('stacked-boundary-slider', 'value')])
def set_num_tads_options(size):
    style = {}
    style['width'] = str(size) + '%'
    style['height'] = str(size) + '%'
    return style


@app.callback(
    Output('Stacked Domain Plot', 'style'),
    [Input('stacked-domain-slider', 'value')])
def set_num_tads_options(size):
    style = {}
    style['width'] = str(size) + '%'
    style['height'] = str(size) + '%'
    return style


@app.callback(
    Output('MoC Comparison Plot', 'style'),
    [Input('moc-compare-slider', 'value')])
def set_num_tads_options(size):
    style = {}
    style['width'] = str(size) + '%'
    style['height'] = str(size) + '%'
    return style


@app.callback(
    Output('MoC Plot', 'style'),
    [Input('moc-average-slider', 'value')])
def set_num_tads_options(size):
    style = {}
    style['width'] = str(size) + '%'
    style['height'] = str(size) + '%'
    return style


# ------------------------------------------------------------------------------
# Plot Generators
# -----------------------------------------------------------------------------

@app.callback(
    [Output("TAD dict", "data"),
     Output("TAD dict binned", "data"),
     Output("Color dict", "data")],
    Input('Normalization', 'value'))
def data_extract(norm_path):
    print("Extracting Data")
    color_itt = 0
    color_dict = OrderedDict()
    tad_dict = OrderedDict()
    tad_dict_binned = OrderedDict()
    for filename in os.listdir(norm_path):
        if not filename.startswith('.') and os.stat(os.path.join(norm_path, filename)).st_size != 0 and "Zone.Identifier" not in str(os.path.basename(filename)):
            with open(os.path.join(norm_path, filename), 'r') as file:
                spamreader = csv.reader(file)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(file.read(1024))
                file.seek(0)
                tad_data = [[digit for digit in line.strip().split(sep=dialect.delimiter)] for line in file]
                if len(tad_data[0]) == 2:
                    tad_data = np.asarray(tad_data, dtype='float')
                elif len(tad_data[0]) == 3:
                    temp_data = []
                    for i in range(len(tad_data)):
                        if tad_data[i][0] == str(chromosome) or tad_data[i][0] == 'chr' + str(chromosome):
                            temp_data.append(tad_data[i][1:])
                    tad_data = np.asarray(temp_data, dtype='float')
            if tad_data.size != 0:
                color_dict[filename[:-4]] = colors[color_itt]
                tad_dict[filename[:-4]] = tad_data
                tad_data = np.asarray(tad_data)
                tad_dict_binned[filename[:-4]] = tad_data / resolution
                color_itt += 1
    return [tad_dict, tad_dict_binned, color_dict]


@app.callback(
    Output("MoC data", "data"),
    [Input('TAD dict binned', 'data')])
def extract_MoC(tad_dict_binned):
    itt = 0
    num_methods = len(tad_dict_binned.keys())
    names = tad_dict_binned.keys()
    if num_methods > 1:
        MoC = [[None for i in range(num_methods)] for j in range(num_methods)]
        for check_file in names:
            check_bed = tad_dict_binned[check_file]
            file_count = 0
            for filename in names:
                if filename == check_file:
                    MoC[itt][file_count] = 1
                else:
                    avg_MoC = []
                    bed = tad_dict_binned[filename]
                    for check_row in check_bed:
                        for row in bed:
                            if check_row[0] < row[1] and check_row[1] > row[0]:
                                if check_row[1] <= row[1] and check_row[0] >= row[0]:
                                    avg_MoC.append(math.pow(check_row[1] - check_row[0], 2) / (
                                            (check_row[1] - check_row[0]) * (row[1] - row[0])))
                                elif check_row[1] <= row[1] and check_row[0] <= row[0]:
                                    avg_MoC.append(math.pow(check_row[1] - row[0], 2) / (
                                            (check_row[1] - check_row[0]) * (row[1] - row[0])))
                                elif check_row[1] >= row[1] and check_row[0] >= row[0]:
                                    avg_MoC.append(math.pow(row[1] - check_row[0], 2) / (
                                            (check_row[1] - check_row[0]) * (row[1] - row[0])))
                                else:
                                    avg_MoC.append(math.pow(row[1] - row[0], 2) / (
                                            (check_row[1] - check_row[0]) * (row[1] - row[0])))
                            else:
                                avg_MoC.append(0)
                    if len(avg_MoC) == 1 and avg_MoC[0] > 0:
                        MoC[itt][file_count] = avg_MoC[0]
                    elif sum(avg_MoC) <= 0:
                        MoC[itt][file_count] = .000001
                    else:
                        MoC[itt][file_count] = sum(avg_MoC) / (math.sqrt(len(avg_MoC)) - 1)
                file_count += 1
            itt += 1
        MoC = np.asarray(MoC)
    return MoC



@app.callback(
    Output("Number TADs Plot", "figure"),
    [Input('TAD dict', 'data'),
     Input('Color dict', 'data'),
     Input('Number TADs Options', 'value')])
def set_display_num_TADs_map(tad_dict, color_dict, number_tads_options):
    print("Construct TAD Size Comparison")
    if number_tads_options:
        number_tads = []
        for filename in number_tads_options:
            bed = tad_dict[filename[:-4]]
            number_tads.append([filename[:-4], len(bed)])
        df = pd.DataFrame(data=number_tads, columns=["Callers", "Number of TADs"])
        size_plot = px.bar(df, x="Callers", y="Number of TADs", color="Callers", color_discrete_map=color_dict,
                           template='simple_white')
    else:
        size_plot = px.bar()
    return size_plot


@app.callback(
    Output("Whisker Plot", "figure"),
    [Input('TAD dict binned', 'data'),
     Input('Color dict', 'data'),
     Input('Whisker Options', 'value')])
def set_display_whisker_map(tad_dict_binned, color_dict, whisker_options):
    print("Construct Whisker Plot")
    size_tads = []
    if whisker_options:
        for filename in whisker_options:
            bed = tad_dict_binned[filename[:-4]]
            for row in bed:
                size_tads.append([filename[:-4], row[1] - row[0]])
        box_df = pd.DataFrame(data=size_tads, columns=["Callers", "Size of TADs"])
        whisker_plot = px.box(box_df, x="Callers", y="Size of TADs", color="Callers", color_discrete_map=color_dict,
                              template='simple_white')
    else:
        whisker_plot = px.box()
    return whisker_plot


@app.callback(
    Output("Boundary Plot", "figure"),
    [Input('TAD dict binned', 'data'),
     Input('Color dict', 'data'),
     Input('Boundary Options', 'value')])
def set_display_boundary_map(tad_dict_binned, color_dict, boundary_option):
    boundaries = []
    if boundary_option:
        selected_option = boundary_option[:-4]
        check_bed = tad_dict_binned[selected_option]
        for tolerance in range(10):
            for key in tad_dict_binned.keys():
                if key not in selected_option:
                    check_boundaries = [True for y in range(len(check_bed) * 2)]
                    shared_boundaries = 0
                    bed = tad_dict_binned[key]
                    for row in bed:
                        itt = 0
                        for check in check_bed:
                            if check_boundaries[itt] and math.isclose(row[0], check[0], abs_tol=tolerance):
                                shared_boundaries += 1
                                check_boundaries[itt] = False
                            if check_boundaries[itt + 1] and math.isclose(row[1], check[1], abs_tol=tolerance):
                                shared_boundaries += 1
                                check_boundaries[itt + 1] = False
                            itt += 2
                    boundaries.append([key, tolerance, shared_boundaries])
        shared_boundaries_df = pd.DataFrame(data=boundaries, columns=["Callers", "Tolerance", "Shared Boundaries"])
        boundary_plot = px.bar(shared_boundaries_df, x="Tolerance", y="Shared Boundaries", color="Callers",
                               barmode='group',
                               color_discrete_map=color_dict, template='simple_white')
    else:
        boundary_plot = px.bar()
    return boundary_plot


@app.callback(
    Output("Stacked Boundary Plot", "figure"),
    [Input('TAD dict binned', 'data'),
     Input('Stacked Boundary Options', 'value')])
def set_display_stacked_boundary_map(tad_dict_binned, stacked_boundary_option):
    tolerance = int(stacked_boundary_option)
    itt = 0
    num_methods = len(tad_dict_binned.keys())
    names = list(tad_dict_binned.keys())
    if num_methods > 1:
        stack = [[0 for x in range(num_methods)] for y in range(num_methods)]
        for check_key in names:
            check_bed = tad_dict_binned[check_key]
            check_boundaries = [[0 for x in range(3)] for y in range(len(check_bed) * 2)]
            for i in range(0, 2 * len(check_bed), 2):
                test = math.floor(i / 2)
                check_boundaries[i][0] = check_bed[test][0]
                check_boundaries[i][1] = 0
                check_boundaries[i][2] = True
                check_boundaries[i + 1][0] = check_bed[test][1]
                check_boundaries[i + 1][1] = 0
                check_boundaries[i+1][2] = True
            for key in names:
                if key != check_key:
                    bed = tad_dict_binned[key]
                    for row in bed:
                        for i in range(0, len(check_boundaries), 2):
                            if check_boundaries[i][2] and \
                                    math.isclose(row[0], check_boundaries[i][0], abs_tol=tolerance):
                                check_boundaries[i][1] += 1
                                check_boundaries[i][2] = False
                            if check_boundaries[i+1][2] and \
                                    math.isclose(row[1], check_boundaries[i+1][0], abs_tol=tolerance):
                                check_boundaries[i+1][1] += 1
                                check_boundaries[i+1][2] = False
                    for i in range(len(check_boundaries)):
                        check_boundaries[i][2] = True
            for i in range(num_methods):
                count = 0
                for j in range(len(check_boundaries)):
                    if check_boundaries[j][1] == i:
                        count += 1
                count = count / len(check_boundaries)
                stack[itt][i] = count
            itt += 1
        stack = np.asarray(stack)
        stacked_boundary_plot = go.Figure(data=[
            go.Bar(name='Unique', x=names, y=stack[:, 0])])
        for i in range(1, len(stack)):
            title = str(i) + " methods"
            stacked_boundary_plot.add_bar(name=title, x=names, y=stack[:, i])
        stacked_boundary_plot.update_layout(barmode='stack', template='simple_white')
        stacked_boundary_plot.update_layout(legend_title_text='Boundaries found in:' , xaxis_title='Callers', yaxis_title='Percent of Shared Boundaries')
    else:
        stacked_boundary_plot = px.bar()
    return stacked_boundary_plot


@app.callback(
    Output("Stacked Domain Plot", "figure"),
    [Input('TAD dict binned', 'data'),
     Input('Stacked Domain Options', 'value')])
def set_display_stacked_Domain_map(tad_dict_binned, stacked_domain_option):
    tolerance = int(stacked_domain_option)
    itt = 0
    num_methods = len(tad_dict_binned.keys())
    names = list(tad_dict_binned.keys())
    if num_methods > 1:
        stack = [[0 for x in range(num_methods)] for y in range(num_methods)]
        for check_key in names:
            check_bed = tad_dict_binned[check_key]
            check_boundaries = [[0 for x in range(3)] for y in range(len(check_bed) * 2)]
            for i in range(0, 2 * len(check_bed), 2):
                test = math.floor(i / 2)
                check_boundaries[i][0] = check_bed[test][0]
                check_boundaries[i][1] = 0
                check_boundaries[i][2] = True
                check_boundaries[i + 1][0] = check_bed[test][1]
                check_boundaries[i + 1][1] = 0
                check_boundaries[i + 1][2] = True
            for key in names:
                if key != check_key:
                    bed = tad_dict_binned[key]
                    for row in bed:
                        for i in range(0, len(check_boundaries), 2):
                            if check_boundaries[i][2] and \
                                    math.isclose(row[0], check_boundaries[i][0], abs_tol=tolerance) and \
                                    math.isclose(row[1], check_boundaries[i + 1][0], abs_tol=tolerance):
                                check_boundaries[i][1] += 1
                                check_boundaries[i + 1][1] += 1
                                check_boundaries[i][2] = False
                    for i in range(len(check_boundaries)):
                        check_boundaries[i][2] = True
            for i in range(num_methods):
                count = 0
                for j in range(len(check_boundaries)):
                    if check_boundaries[j][1] == i:
                        count += 1
                count = count / len(check_boundaries)
                stack[itt][i] = count
            itt += 1
        stack = np.asarray(stack)
        stacked_domain_plot = go.Figure(data=[
            go.Bar(name='Unique', x=names, y=stack[:, 0])])
        for i in range(1, len(stack)):
            title = str(i) + " methods"
            stacked_domain_plot.add_bar(name=title, x=names, y=stack[:, i])
        stacked_domain_plot.update_layout(barmode='stack', template='simple_white')
        stacked_domain_plot.update_layout(legend_title_text='Domains found in:', xaxis_title='Callers', yaxis_title='Percent of Shared Domains')
    else:
        stacked_domain_plot = px.bar()
    return stacked_domain_plot


@app.callback(
    Output("MoC Comparison Plot", "figure"),
    [Input('MoC data', 'data'),
     Input('TAD dict binned', 'data'),
     Input('MoC Options', 'value')])
def set_MoC_Comparison(MoC, tad_dict_binned, MoC_option):
    print("Construct MoC_Comparison")
    print(MoC)
    MoC_Comparison_plot = px.bar()
    names = list(tad_dict_binned.keys())
    if len(MoC) > 1:
        row_select = 0
        i = 0
        for filename in names:
            if filename in MoC_option:
                row_select = i
            i += 1
        MoC_Comparison_plot.add_bar(x=names, y=MoC[row_select])
        MoC_Comparison_plot.update_layout(template='simple_white')
        MoC_Comparison_plot.update_yaxes(title_text="Measure of Concordance")
        MoC_Comparison_plot.update_xaxes(title_text="Callers")
    else:
        MoC_Comparison_plot = px.bar()
    return MoC_Comparison_plot


@app.callback(
    Output("MoC Plot", "figure"),
    [Input('MoC data', 'data'),
     Input('TAD dict binned', 'data')])
def set_MoC(MoC, tad_dict_binned):
    names = list(tad_dict_binned.keys())
    MoC_plot = px.bar()
    if len(MoC) > 1:
        average = []
        for row in MoC:
            average.append(sum(row) / len(row))
        MoC_plot.add_bar(x=names, y=average)
        MoC_plot.update_layout(template='simple_white')
        MoC_plot.update_yaxes(title_text="Average Measure of Concordance")
        MoC_plot.update_xaxes(title_text="Callers")
    else:
        MoC_plot = px.bar()
    return MoC_plot


@app.callback(
    Output("TSNE Plot", "figure"),
    [Input('MoC data', 'data'),
     Input('TAD dict binned', 'data'),
     Input("tnse-marker-slider", "value"),
     Input('TSNE Slider', 'value')])
def set_TNSE(MoC, tad_dict_binned, markersize, slider):
    names = list(tad_dict_binned.keys())
    if len(MoC) > 1:
        person_matrix = np.corrcoef(MoC)
        tsne_pca = TSNE(n_components=2, perplexity=slider, method='exact', init='pca')
        tsne_random = TSNE(n_components=2, perplexity=slider, method='exact', init='random')
        projections_pca = tsne_pca.fit_transform(person_matrix)
        projections_random = tsne_random.fit_transform(person_matrix)
        TNSE_plot = make_subplots(rows=2, cols=1, vertical_spacing=0.25,
                                  subplot_titles=('Initial Embedding: PCA', 'Initial Embedding: Random'))
        for i in range(len(names)):
            TNSE_plot.add_trace(go.Scatter(
                x=[projections_pca[i][0]], y=[projections_pca[i][1]], mode='markers',
                marker_color=colors[i], marker_size=markersize, text=names[i], name=names[i]
            ), row=1, col=1)
            TNSE_plot.add_trace(go.Scatter(
                x=[projections_random[i][0]], y=[projections_random[i][1]], mode='markers',
                marker_color=colors[i], marker_size=markersize, text=names[i], name=names[i], showlegend=False
            ), row=2, col=1)
        TNSE_plot.update_layout(template='simple_white')
    else:
        TNSE_plot = px.bar()
    return TNSE_plot


@app.callback(
    Output("PCA Plot", "figure"),
    [Input('MoC data', 'data'),
     Input('TAD dict binned', 'data'),
     Input("pca-marker-slider", "value"),
     Input('Normalization', 'value')])
def set_PCA(MoC, tad_dict_binned, markersize, norm_path):
    names = list(tad_dict_binned.keys())
    if len(os.listdir(norm_path)) > 1:
        person_matrix = np.corrcoef(MoC)
        pca = PCA(n_components=2, random_state=0)
        projections = pca.fit_transform(person_matrix)
        PCA_plot = px.scatter(
            projections, x=0, y=1,
            color=names, labels={'color': 'Methods'},
            color_discrete_sequence=colors
        )
        PCA_plot.update_traces(marker=dict(size=markersize))
        PCA_plot.update_layout(template='simple_white')
        PCA_plot.update_layout(xaxis_title='Principal Component 1', yaxis_title='Principal Component 2')
    else:
        PCA_plot = px.bar()
    return PCA_plot


def save_file(name, content, norm):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(norm, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


if __name__ == "__main__":
    app.run_server(
        debug=True,
        port=8050,
        host='0.0.0.0'
    )
