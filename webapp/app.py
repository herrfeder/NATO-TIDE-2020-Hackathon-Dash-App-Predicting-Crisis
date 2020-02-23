import os
import pathlib
import re
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import cufflinks as cf
from matplotlib import cm
from matplotlib import colors
from scipy import interpolate
import plotly.graph_objs as go

# Initialize app

app = dash.Dash(
    __name__,
    url_base_pathname='/predictingcrisis/',
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

# Load data

APP_PATH = str(pathlib.Path(__file__).parent.resolve())


df_acled = pd.read_csv(
    os.path.join(APP_PATH, os.path.join("data", "acled_social_iso3.csv"))
)

df_short = df_acled[['YEAR',
    'COUNTRY',                 
    'Life expectancy at birth, total (years)', 
    'GDP (current US$)',
    'Death rate, crude (per 1,000 people)', 
    'Population growth (annual %)',
    'Urban population (% of total)',
    'Central government, Fiscal Balance (Current US $)',
    'Population, Total','lat', 'lon',
    ]].drop_duplicates()


text_template = """
Country: {country}<br>
Life expectancy: {life_exp}<br>
GDP: {gdp}<br>
Death Rate: {deathr}<br>
Gov fiscal balance: {fisc}<br>
Urban Pop (%): {urbanpop}<br>
Pop Growth (%): {popgrowth}
"""

fat_bins = list(range(0,2000,100))
fat_labels = [str(x) for x in fat_bins[1:]]
df_acled["FAT_bin"] = pd.cut(df_acled['FATALITIES'], fat_bins, labels=fat_labels)
df_acled["FAT_bin"] = df_acled["FAT_bin"].cat.add_categories("< 100")
df_acled["FAT_bin"].fillna("< 100", inplace=True)
df_acled["FAT_bin"] = df_acled["FAT_bin"].replace("", "< 100")
fat_labels = ["< 100"] + fat_labels
fat_labels = ["notfound"] + fat_labels


bat_bins = list(range(0,200,10))
bat_labels = [str(x) for x in fat_bins[1:]]
df_acled["BAT_bin"] = pd.cut(df_acled['Battles'], bat_bins, labels=bat_labels)
df_acled["BAT_bin"] = df_acled["BAT_bin"].cat.add_categories("< 10")
df_acled["BAT_bin"].fillna("< 10", inplace=True)
df_acled["BAT_bin"] = df_acled["BAT_bin"].replace("", "< 10")
bat_labels = ["< 10"] + bat_labels
bat_labels = ["notfound"] + bat_labels


vio_bins = list(range(0,200,10))
vio_labels = [str(x) for x in vio_bins[1:]]
df_acled["VIO_bin"] = pd.cut(df_acled["Violence against civilians"], vio_bins, labels=vio_labels)
df_acled["VIO_bin"] = df_acled["VIO_bin"].cat.add_categories("< 10")
df_acled["VIO_bin"].fillna("< 10", inplace=True)
df_acled["VIO_bin"] = df_acled["VIO_bin"].replace("", "< 10")
vio_labels = ["< 10"] + vio_labels
vio_labels = ["notfound"] + vio_labels


with open(os.path.join(APP_PATH, os.path.join("data", "countries.geo.json"))) as json_file:
    world_geo = json.load(json_file)

COUNTRIES = list(df_acled.COUNTRY.unique())
ISO3 = list(df_acled.iso3.unique())

c_i_dict = dict(zip(ISO3, COUNTRIES))

country_labels = []
for country in COUNTRIES:
    country_labels.append({"label": country,
                          "value": country,
                        })
    
country_labels.append({"label": "All", "value": "All"})

MONTHS = list(df_acled.EVENT_DATE_MONTH.unique())
MONTH_LIST = list(range(len(MONTHS)))

YEARS = list(df_acled.YEAR.unique())
YEAR_LIST = list(range(len(YEARS)))


DEFAULT_COLORSCALE = [
"#3b3b3d",
"#8000ff",
"#6629fe",
"#4c50fc",
"#3079f7",
"#169bf2",
"#07bbea",
"#20d5e1",
"#3dead5",
"#56f7ca",
"#72febb",
"#8cfead",
"#a8f79c",
"#c2ea8c",
"#ded579",
"#f9bb66",
"#ff9b52",
"#ff793e",
"#ff5029",
"#ff2914",
"#ff0000",
]


DEFAULT_OPACITY = 0.5

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo",width="100px", height="200px", src="https://www.nicepng.com/png/detail/21-216488_tis-but-a-scratch-butchers-tears.png"),
                html.H4(children="TIDE Hackathon Predicting Crisis in AFRICA"),
                html.P(
                    id="description",
                    children="This shows the monthly data for different metrics over all african countries",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the Month: ",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=MONTH_LIST[0],
                                    max=MONTH_LIST[-1],
                                    value=MONTH_LIST[0],
                                    marks={
                                        str(month): {
                                            "label": str(month),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for month in MONTHS
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Heatmap for African Countries in Month {0}".format(
                                        MONTHS[0]
                                    ),
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=dict(
                                        data=[
                                            dict(
                                                lat=df_short[df_short["YEAR"] == YEARS[0]]['lat'],
                                                lon=df_short[df_short["YEAR"] == YEARS[0]]['lon'],
                                                text=df_short[df_short["YEAR"] == YEARS[0]]['COUNTRY'],
                                                type="choroplethmapbox",
                                            )
                                        ],
                                        layout=dict(
                                            mapbox=dict(
                                                #layers=[{
                                                    #'source': world_geo,
                                                    #'type': "fill", 'below': "traces", 'color': "royalblue", "opacity": .30,}],
                                                accesstoken=mapbox_access_token,
                                                style=mapbox_style,
                                                center=dict(
                                                    lat=20.780772, lon=8.789063
                                                ),
                                                pitch=0,
                                                zoom=2,
                                            ),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select chart:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Fatalities",
                                    "value": "FATALITIES",
                                },
                                {
                                    "label": "Battles",
                                    "value": "Battles",
                                },
                                {
                                    "label": "Violence against civilians",
                                    "value": "Violence against civilians",
                                },
                                {
                                    "label": "XGBoost_riots",
                                    "value": "xgboost_riots",
                                },
                                {
                                    "label": "XGBoost_battles",
                                    "value": "xgboost_battles",
                                },
                                {
                                    "label": "rnf_battles",
                                    "value": "rnf_battles",
                                },
                                {
                                    "label": "rnf_riots",
                                    "value": "rnf_riots",
                                },
                            ],
                            value="FATALITIES",
                            id="chart-dropdown",
                        ),
                            html.Div([
                                html.P(id="country-selector", children="Select Country:"),
                                    dcc.Dropdown(
                                        options=country_labels,
                                        value="All",
                                        id="country-dropdown",
                                    ),
                            ], style={"padding-bottom":"0px"}),
                        dcc.Graph(
                            id="selected-data",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#F4F4F8",
                                    plot_bgcolor="#F4F4F8",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
               
        
                html.Div(
                    id="correlation-container",
                    style={'width':'100%', 'display': 'inline-block', 'vertical-align': 'middle'},
                    children=[
                   
                        dcc.Graph(
                            id="country-corr",
                            style={'height':'1200px'},
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#F4F4F8",
                                    plot_bgcolor="#F4F4F8",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
        
        html.Div(
                    id="evaluation-container",
                    style={'width':'100%', 'vertical-align': 'middle', 'padding-top':'40px'},
                    children=[
                        html.Div(children=[
                            html.Div([
                                dcc.Graph(
                                    id="eval-plot-1",
                                    figure=dict(
                                        data=[dict(x=0, y=0)],
                                        layout=dict(
                                            paper_bgcolor="#F4F4F8",
                                            plot_bgcolor="#F4F4F8",
                                            autofill=True,
                                            margin=dict(t=75, r=50, b=100, l=50),
                                        ),
                                    ),
                                )],style={'width':'45%'}, className="six columns"
                            ),
                            html.Div([
                                dcc.Graph(
                                    id="eval-plot-2",
                                    figure=dict(
                                        data=[dict(x=0, y=0)],
                                        layout=dict(
                                            paper_bgcolor="#F4F4F8",
                                            plot_bgcolor="#F4F4F8",
                                            autofill=True,
                                            margin=dict(t=75, r=50, b=100, l=50),
                                        ),
                                    ),
                                )], style={'width':'45%'},  className="six columns"
                            ),
                            ],className='row'),
                        html.Div(children=[
                            html.Div([
                                dcc.Graph(
                                    id="eval-plot-3",
                                    figure=dict(
                                        data=[dict(x=0, y=0)],
                                        layout=dict(
                                            paper_bgcolor="#F4F4F8",
                                            plot_bgcolor="#F4F4F8",
                                            autofill=True,
                                            margin=dict(t=75, r=50, b=100, l=50),
                                        ),
                                    ),
                                )],style={'width':'45%'}, className="six columns"
                            ),
                            html.Div([
                                dcc.Graph(
                                    id="eval-plot-4",
                                    figure=dict(
                                        data=[dict(x=0, y=0)],
                                        layout=dict(
                                            paper_bgcolor="#F4F4F8",
                                            plot_bgcolor="#F4F4F8",
                                            autofill=True,
                                            margin=dict(t=75, r=50, b=100, l=50),
                                        ),
                                    ),
                                )], style={'width':'45%'},  className="six columns"
                            ),
                            ],className='row', style={'padding-top':'20px'}),
                        
                    ],
                ),
            
        
    ],
)


@app.callback(
    Output("eval-plot-1", "figure"),
    [Input("chart-dropdown", "value")],
    [State("eval-plot-1", "figure")],
   
)
def display_eval_1(chart, figure):

    conf = pd.read_csv(
            os.path.join(APP_PATH,"data/confusion_mat_xgb_label0.csv"))

    title = "XGBoost Confusion Matrix for Battles Label"
    y = conf["Unnamed: 0"].to_list()
    conf.drop(columns=["Unnamed: 0"], inplace=True)
    x = list(conf.columns)
    coordinates = conf.values.tolist()

    trace1 = {
                "type": "heatmap", 
                "x": x, 
                "y": y, 
                "z": coordinates,
                "colorscale": 'viridis'
    }

    data = trace1

    layout = {"title": title}
    fig = go.Figure(dict(data=data, layout=layout))

    layout = fig["layout"]

    layout["paper_bgcolor"] = "#1f2630"
    layout["plot_bgcolor"] = "#1f2630"
    layout["font"]["color"] = "#2cfec1"
    layout["title"]["font"]["color"] = "#2cfec1"
    layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["xaxis"]["gridcolor"] = "#5b5b5b"
    layout["yaxis"]["gridcolor"] = "#5b5b5b"
    layout["margin"]["t"] = 75
    layout["margin"]["r"] = 50
    layout["margin"]["b"] = 100
    layout["margin"]["l"] = 50

    return go.Figure(fig)
 
@app.callback(
    Output("eval-plot-2", "figure"),
    [Input("chart-dropdown", "value")],
    [State("eval-plot-2", "figure")],
   
)
def display_eval_2(chart, figure):

    conf = pd.read_csv(
                os.path.join(APP_PATH,"data/confusion_mat_xgb_label1.csv"))
    title = "XGBoost Confusion Matrix for Riot Label"
    y = conf["Unnamed: 0"].to_list()
    conf.drop(columns=["Unnamed: 0"], inplace=True)
    x = list(conf.columns)
    coordinates = conf.values.tolist()

    trace1 = {
                "type": "heatmap", 
                "x": x, 
                "y": y, 
                "z": coordinates,
                "colorscale": 'viridis'
    }

    data = trace1

    layout = {"title": title}
    fig = go.Figure(dict(data=data, layout=layout))

    layout = fig["layout"]

    layout["paper_bgcolor"] = "#1f2630"
    layout["plot_bgcolor"] = "#1f2630"
    layout["font"]["color"] = "#2cfec1"
    layout["title"]["font"]["color"] = "#2cfec1"
    layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["xaxis"]["gridcolor"] = "#5b5b5b"
    layout["yaxis"]["gridcolor"] = "#5b5b5b"
    layout["margin"]["t"] = 75
    layout["margin"]["r"] = 50
    layout["margin"]["b"] = 100
    layout["margin"]["l"] = 50

    return go.Figure(fig)
     

@app.callback(
    Output("eval-plot-3", "figure"),
    [Input("chart-dropdown", "value")],
    [State("eval-plot-3", "figure")],
   
)
def display_eval_3(chart, figure):
    
    conf = pd.read_csv(
        os.path.join(APP_PATH,"data/ConfusionMatrix_MyLabels_rndForest.csv"))
    title = "Random Forest Confusion Matrix for own Labels"
    
    print(conf)
    y = conf["Unnamed: 0"].to_list()
    conf.drop(columns=["Unnamed: 0"], inplace=True)
    x = list(conf.columns)
    coordinates = conf.values.tolist()

    trace1 = {
                "type": "heatmap", 
                "x": x, 
                "y": y, 
                "z": coordinates,
                "colorscale": 'viridis'
    }

    data = trace1

    layout = {"title": title}
    fig = go.Figure(dict(data=data, layout=layout))

    layout = fig["layout"]

    layout["paper_bgcolor"] = "#1f2630"
    layout["plot_bgcolor"] = "#1f2630"
    layout["font"]["color"] = "#2cfec1"
    layout["title"]["font"]["color"] = "#2cfec1"
    layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["xaxis"]["gridcolor"] = "#5b5b5b"
    layout["yaxis"]["gridcolor"] = "#5b5b5b"
    layout["margin"]["t"] = 75
    layout["margin"]["r"] = 50
    layout["margin"]["b"] = 100
    layout["margin"]["l"] = 50

    return go.Figure(fig)
  
@app.callback(
    Output("eval-plot-4", "figure"),
    [Input("chart-dropdown", "value")],
    [State("eval-plot-4", "figure")],
   
)
def display_eval_4(chart, figure):
    
    conf = pd.read_csv(
       os.path.join(APP_PATH,"data/ConfusionMatrix_rndForest.csv"))
    title = "Random Forest Confusion Matrix for provided Labels"
    
    print(conf)
    y = conf["Unnamed: 0"].to_list()
    conf.drop(columns=["Unnamed: 0"], inplace=True)
    x = list(conf.columns)
    coordinates = conf.values.tolist()

    trace1 = {
                "type": "heatmap", 
                "x": x, 
                "y": y, 
                "z": coordinates,
                "colorscale": 'viridis'
    }

    data = trace1

    layout = {"title": title}
    fig = go.Figure(dict(data=data, layout=layout))

    layout = fig["layout"]

    layout["paper_bgcolor"] = "#1f2630"
    layout["plot_bgcolor"] = "#1f2630"
    layout["font"]["color"] = "#2cfec1"
    layout["title"]["font"]["color"] = "#2cfec1"
    layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["xaxis"]["gridcolor"] = "#5b5b5b"
    layout["yaxis"]["gridcolor"] = "#5b5b5b"
    layout["margin"]["t"] = 75
    layout["margin"]["r"] = 50
    layout["margin"]["b"] = 100
    layout["margin"]["l"] = 50

    return go.Figure(fig)

@app.callback(
    Output("country-corr", "figure"),
    [Input("country-dropdown", "value")],
    [State("country-corr", "figure")],
)
def display_corr(chart, figure):
    
    try:
        df_acled.drop(columns=['Unnamed: 0', 
                               'Unnamed: 0.1',
                               'Unnamed: 0.1.1',
                               'Unnamed: 0.1.1.1'], inplace=True)
    except:
        pass
    
    if chart=="All":
        corr = df_acled.corr()
        coordinates = corr.values.tolist()
        columns = list(corr.columns)
    else:
        corr = df_acled[df_acled['COUNTRY'] == chart].corr()
        coordinates = corr.values.tolist()
        columns = list(corr.columns)
    
    trace1 = {
        "type": "heatmap", 
        "x": columns, 
        "y": columns, 
        "z": coordinates,
        "colorscale": 'viridis'
        }
    
    data = trace1
    
    layout = {"title": "Features Correlation Matrix per Country"}
    fig = go.Figure(dict(data=data, layout=layout))
    
    layout = fig["layout"]
    
    layout["paper_bgcolor"] = "#1f2630"
    layout["plot_bgcolor"] = "#1f2630"
    layout["font"]["color"] = "#2cfec1"
    layout["title"]["font"]["color"] = "#2cfec1"
    layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    layout["xaxis"]["gridcolor"] = "#5b5b5b"
    layout["yaxis"]["gridcolor"] = "#5b5b5b"
    layout["margin"]["t"] = 75
    layout["margin"]["r"] = 50
    layout["margin"]["b"] = 100
    layout["margin"]["l"] = 50
    
    return go.Figure(fig)


@app.callback(
    Output("selected-data", "figure"),
    [Input("chart-dropdown", "value"),
     Input("country-dropdown", "value")],
    [State("selected-data", "figure")],
)
def display_plot(chart, country,figure):
    if (chart.startswith("xgboost")) or (chart.startswith("rnf")):
        return
    if country=="All":
        fig = go.Figure([go.Scatter(x=df_acled['EVENT_DATE_MONTH'], y=df_acled[chart])])
        fig_layout = fig["layout"]
        fig_data = fig["data"]
        fig_layout["title"] = "{} between 1997-2020 for all Countries".format(chart)

    else:
        fig = go.Figure([go.Scatter(x=df_acled[df_acled["COUNTRY"] == country]['EVENT_DATE_MONTH'], y=df_acled[df_acled["COUNTRY"] == country][chart])])
        fig_layout = fig["layout"]
        fig_data = fig["data"]
        fig_layout["title"] = "{} between 1997-2020 for {}".format(chart, country)
    
    fig_data[0]["marker"]["color"] = "#2cfec1"
    fig_data[0]["marker"]["opacity"] = 1
    fig_data[0]["marker"]["line"]["width"] = 0
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#2cfec1"
    fig_layout["title"]["font"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["margin"]["t"] = 75
    fig_layout["margin"]["r"] = 50
    fig_layout["margin"]["b"] = 100
    fig_layout["margin"]["l"] = 50
    
    return fig

@app.callback(
    Output("county-choropleth", "figure"),
    [Input("years-slider", "value"),
    Input("chart-dropdown", "value"),
    Input("country-dropdown", "value")],
    [State("county-choropleth", "figure")],
)
def display_map(year, chart, country,figure):
    if chart=="FATALITIES":
        column = "FAT_bin"
        labels = fat_labels
    elif chart=="Battles":
        column = "BAT_bin"
        labels = bat_labels
    elif chart== "Violence against civilians":
        column = "VIO_bin"
        labels = vio_labels
    
    elif chart == "xgboost_riots":
        column = "protest_riots_case"
        labels = ["0", "1"]
        pred_df = pd.read_csv(
            os.path.join(APP_PATH,"data/results_xgb_classifier_hackathon_labels_lookback_6m.csv"))

    
    elif chart == "xgboost_battles":
        column = "battle_case"
        labels = ["0", "1"]
        pred_df = pd.read_csv(
            os.path.join(APP_PATH,"data/results_xgb_classifier_hackathon_labels_lookback_6m.csv"))

     
    elif chart == "rnf_riots":
        column = "protest_riots_case"
        labels = ["0", "1"]
        pred_df = pd.read_csv(
            os.path.join(APP_PATH,"data/Future_NatoDefinitionCrisis_rnd_forest.csv"))

    
    elif chart == "rnf_battles":
        column = "battle_case"
        labels = ["0", "1"]
        pred_df = pd.read_csv(
            os.path.join(APP_PATH,"data/Future_NatoDefinitionCrisis_rnd_forest.csv"))

        
    cm = dict(zip(labels, DEFAULT_COLORSCALE))
    print(year)
    YEAR = int(MONTHS[year].split('-')[0])
    data = [
        dict(
            lat=df_short[df_short["YEAR"] == YEAR]['lat'],
            lon=df_short[df_short["YEAR"] == YEAR]['lon'],
            text=df_short[df_short["YEAR"] == YEAR]['COUNTRY'],
            type="scattermapbox",
            marker=dict(size=5, color="white", opacity=0),
        )
    ]
        
    if chart.startswith("xgboost"):
        annotations = [
            dict(
                showarrow=False,
                align="right",
                text="<b>Future Prediction of {}</b>".format(chart),
                font=dict(color="#2cfec1"),
                bgcolor="#1f2630",
                x=0.95,
                y=0.95,
            )
        ]

        for i, label in enumerate(labels):
                color = cm[label]
                annotations.append(
                    dict(
                        arrowcolor=color,
                        text=label,
                        x=0.95,
                        y=0.85 - (i / 20),
                        ax=-60,
                        ay=0,
                        arrowwidth=5,
                        arrowhead=0,
                        bgcolor="#1f2630",
                        font=dict(color="#2cfec1"),
                )
            )
    else:
        annotations = [
            dict(
                showarrow=False,
                align="right",
                text="<b>Categories of {}<br>per Month</b>".format(chart),
                font=dict(color="#2cfec1"),
                bgcolor="#1f2630",
                x=0.95,
                y=0.95,
            )
        ]

        for i, label in enumerate(labels):
                color = cm[label]
                annotations.append(
                    dict(
                        arrowcolor=color,
                        text=label,
                        x=0.95,
                        y=0.85 - (i / 20),
                        ax=-60,
                        ay=0,
                        arrowwidth=5,
                        arrowhead=0,
                        bgcolor="#1f2630",
                        font=dict(color="#2cfec1"),
                )
            )
    
    if "layout" in figure:
        lat = figure["layout"]["mapbox"]["center"]["lat"]
        lon = figure["layout"]["mapbox"]["center"]["lon"]
        zoom = figure["layout"]["mapbox"]["zoom"]
    else:
        lat = (20.780772,)
        lon = (8.789063,)
        zoom = 3

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            center=dict(lat=lat, lon=lon),
            zoom=zoom,
        ),
        hovermode="closest",
        margin=dict(r=0, l=0, t=0, b=0),
        annotations=annotations,
        dragmode="lasso",
    )
        
    iso3_list = list(df_acled.iso3.unique())
    
    if (chart.startswith("xgboost")) or (chart.startswith("rnf")):    
        for val in world_geo['features']:
            if val['id'] in iso3_list:
             
               
                    
                tempval = pred_df[(pred_df["iso3"] == val["id"])][column].values
                try:
                    value = str(int(tempval[0]))
                except:
                    value = str(int(0))

                geo_layer = dict(
                        sourcetype="geojson",
                        source=val,
                        type="fill",
                        color=cm[value],
                        hover="blah",
                        opacity=DEFAULT_OPACITY,
                        fill=dict(outlinecolor="red"),
                )
                layout["mapbox"]["layers"].append(geo_layer)
    else:
        
        for val in world_geo['features']:
            if val['id'] in iso3_list:
                if country == c_i_dict[val['id']]:
                    fill_ob = dict(outlinecolor="white")
                    opacity = 1
                else:
                    fill_ob = ""
                    opacity = DEFAULT_OPACITY
                    
                tempval = df_acled[(df_acled["iso3"] == val["id"]) & (df_acled["EVENT_DATE_MONTH"] == MONTHS[year])][column].values
                try:
                    value = tempval[0]
                except:
                    value = "notfound"

                geo_layer = dict(
                        sourcetype="geojson",
                        source=val,
                        type="fill",
                        color=cm[value],
                        hover="blah",
                        opacity=opacity,
                        fill=fill_ob,
                )
                layout["mapbox"]["layers"].append(geo_layer)
    
    
    fig = dict(data=data, layout=layout)
    return fig


@app.callback(Output("heatmap-title", "children"), 
              [Input("years-slider", "value"),
              Input("chart-dropdown", "value")])
def update_map_title(year, chartvalue):
    if (chartvalue.startswith("xgboost")) or (chartvalue.startswith("rnf")):    
        return "{} for FUTURE".format(chartvalue, MONTHS[year])
    else:
        return "{} for Month {}".format(chartvalue, MONTHS[year])

@app.callback(Output("slider-text", "children"), [Input("years-slider", "value")])
def update_drag_val(year):
    return "Drag the slider to change the Month: {0}".format(MONTHS[year])

@app.callback(Output("description", "children"), 
              [Input("chart-dropdown", "value")])
def update_explanation(chartvalue):
    exp_dict = {}
    exp_dict["Battles"] = "BATTLES means heavy crisis with potential involvement of military"
    exp_dict["FATALITIES"] = "FATALITIES is the number of deaths"
    exp_dict["Violence against civilians"] = "VIOLENCE AGAINST CIVILIANS means surpression by federal authorities"
    exp_dict["rnf_battles"] = "RNF_BATTLES means RANDOM FOREST CLASSIFICATION for potential BATTLES that will occur in the future"
    exp_dict["rnf_riots"] = "RNF_RIOTS means RANDOM FOREST CLASSIFICATION for potential RIOTS that will occur in the future"
    exp_dict["xgboost_battles"] = "XGBOOST_BATTLES means XGBOOST CLASSIFICATION for potential BATTLES that will occur in the future"
    exp_dict["xgboost_riots"] = "XGBOOST_RIOTS means XGBOOST CLASSIFICATION for potential RIOTS that will occur in the future"
    
    
    return "{}".format(exp_dict[chartvalue]) 



if __name__ == "__main__":
    app.run_server(debug=True,  port=8000, host="0.0.0.0")
