# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc # for Graphs
import dash_html_components as html
import dash_table
import pandas as pd
# for date-Slider
import math

#for map
import plotly.graph_objs as go

df = pd.read_csv('csv/main_database.csv')


app = dash.Dash(__name__)


# Load styles
#css_url = 'https://codepen.io/IvanNieto/pen/bRPJyb.css'
css_url = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
css_bootstrap_url = 'https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
app.css.append_css({
    "external_url": [css_bootstrap_url, css_url],
})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# for date-Slider
uniqueYear = set()
for date in df['Date'].unique():
    if type(date) == float and not math.isnan(date):
        uniqueYear.add(int(date))
    elif type(date) == str and date[-4:].isdigit():
        uniqueYear.add(int(date[-4:]))
uniqueYear = sorted(uniqueYear)

yearDict = {}
keys = range(len(uniqueYear))
for i in keys:
    yearDict[i] = uniqueYear[i]


# for map
mapbox_access_token ="pk.eyJ1Ijoic2Z4aWEiLCJhIjoiY2p0eXFmbXhkMThwczN5cnpoY3V2NXM2OSJ9.y1v1n6o9IQ8q-7xiYE6zNw"

# Layout
app.layout = html.Div(children=[
    html.H1(
        children='Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'margin-top': 10,
        }
    ),

    html.H6(
        children='A research dashboard for Indigeneity/Urban Ecology courses',
        style={
        'textAlign': 'center',
        'color': colors['text'],
        'padding': 5,
    }),

    html.Div(
        className='container-fluid',
        children=[
            html.Div(
                # Slider
                className='container',
                children=[
                    html.Div(
                        children=[
                            dcc.Slider(
                                id='slider',
                                min=0,
                                max=len(uniqueYear),
                                marks={str(k):str(v) for k, v in yearDict.items()},
                                # min=min(uniqueYear),
                                # max=max(uniqueYear),
                                # marks={str(date):str(date) for date in uniqueYear},
                                value=len(uniqueYear),
                            )
                        ]
                    ),
                ],
                style={
                    'margin-bottom':'50px',
                }
            ),

            html.Div(
                className='row',
                children=[
                    html.Div(
                        # map
                        className='col-sm-6',
                        children=[
                            dcc.Graph(
                                id="map",
                                config={
                                    'scrollZoom': True
                                },
                                # figure={
                                #         'data': data,
                                #         'layout':map_layout
                                # },
                            ),
                        ]
                    ),

                    html.Div(
                        # Data table
                        className='col-sm-6',
                        id='datatable',
                    ),
                ]
            )
        ]
    ),
])

@app.callback(
    Output('datatable', 'children'),
    [Input('slider', 'value')])
def update_table(value):
    # print("value:",value)
    if value == 26:
        newdf = df
    else:
        newdf = df[df.Date.str.contains(str(yearDict[value]), na=False)]

    table = dash_table.DataTable(
        id='table',
        data=newdf.to_dict("rows"),
        columns=[{"name": i, "id": i} for i in newdf.columns if i not in ["Image", "Column", "Longitude", "Latitude"]],
        n_fixed_rows=1,
        sorting=True,
        filtering=True,
        pagination_mode="fe",
                pagination_settings={
                    "displayed_pages": 1,
                    "current_page": 0,
                    "page_size": 35,
                },
                navigation="page",
        style_cell={
            'whiteSpace': 'normal',
            'padding': '5px',
            'minWidth': '150px',
            'width': '150px',
            'maxWidth': '150px',
            'textAlign': 'left',
        },
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_table={
            'overflowX': 'scroll', # Horizontal scroll
            'maxHeight': '500',
        },
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
    )
    return table


@app.callback(
    Output('map', 'figure'),
    [Input('slider', 'value')])
def update_map(value):
    print("year: ", value)
    if value == 26:
        newdf = df
    else:
        newdf = df[df.Date.str.contains(str(yearDict[value]), na=False)]

    updated_data = [
        go.Scattermapbox(
            lat=newdf['Latitude'],
            lon=newdf['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=newdf['Name']
        )
    ]

    layout = dict(
        #autosize= True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            #bearing=0,
            center=dict(lat=-38.92, lon=174.88),
            pitch=0,
            zoom=4,
        ),
        margin = dict(r=40, l=40, t=40, b=40),
        uirevision='same',
    )

    fig=dict(data=updated_data, layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
