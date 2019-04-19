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

#django
from django_plotly_dash import DjangoDash

df = pd.read_csv('Django_Dash_app/dashplotly/csv/main_database.csv')

#df = pd.read_csv('./csv/main_database.csv')

app = DjangoDash('Dashboard')
#app=dash.Dash(__name__)
#print (app)


# Load styles
#css_url = 'https://codepen.io/IvanNieto/pen/bRPJyb.css'
css_url = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True

#css_url='https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
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

#for Checklist on Type
uniqueType = set()
for type in df['Type'].unique():
    uniqueType.add(str(type))
uniqueType = sorted(uniqueType)

TypeDict = {}
keys = range(len(uniqueType))
for i in keys:
    TypeDict[i] = uniqueType[i]

#print(TypeDict)
#print(TypeDict.items)

checklist_options=[]

for key, value in TypeDict.items():
    option={}
    option['label']=str(value)
    option['value']=str(value)
    checklist_options.append(option)

#print("checklist_options \n", checklist_options)


# for map
mapbox_access_token ="pk.eyJ1Ijoic2Z4aWEiLCJhIjoiY2p0eXFmbXhkMThwczN5cnpoY3V2NXM2OSJ9.y1v1n6o9IQ8q-7xiYE6zNw"

# Layout
app.layout = html.Div(children=[


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
                className='col-sm-4 checklist',
                children=[
                    dcc.Checklist(
                        id="TypeChecklist",
                        options=checklist_options[5:25],
                        values=[]
                    ),

                ]),


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
    [Input('slider', 'value'),
    Input('TypeChecklist','values')])

def update_table(value,types):
    # print("value:",value)
    if value == 26:
        newdf = df
    else:
        newdf = df[df.Date.str.contains(str(yearDict[value]), na=False)]

    finaldf=pd.DataFrame()

    if types == []:
        finaldf = newdf
    else:
        for type in types:
            finaldf = finaldf.append(newdf.loc[newdf['Type']==type])

    table = dash_table.DataTable(
        id='table',
        data=finaldf.to_dict("rows"),
        columns=[{"name": i, "id": i} for i in finaldf.columns if i not in ["Image", "Column", "Longitude", "Latitude"]],
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

        style_cell_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
         }],

        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],

        virtualization=True,
    )
    return table


@app.callback(
    Output('map', 'figure'),
    [Input('slider', 'value'),
    Input('TypeChecklist','values')])
def update_map(year,types):
    print("year: ", year)
    print('types:',types)
    if year == 26:
        newdf = df
    else:
        newdf = df[df.Date.str.contains(str(yearDict[year]), na=False)]

    finaldf=pd.DataFrame()

    if types == []:
        finaldf = newdf
    else:
        for type in types:
            finaldf = finaldf.append(newdf.loc[newdf['Type']==type])


    print(finaldf)

            



    updated_data = [
        go.Scattermapbox(
            lat=finaldf['Latitude'],
            lon=finaldf['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=11,
                opacity=0.7,
             ),
            text= finaldf['Name'],
        ),
    ]

    layout = dict(
        #autosize= True,
        hovermode='closest',
        showlegend=False,
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


"""
if __name__ == '__main__':
    app.run_server(debug=True)

"""
