# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc # for Graphs
import dash_html_components as html
import dash_table
import pandas as pd

#for map
import plotly.graph_objs as go

#for timeline
from Django_Dash_app.dashplotly.uniqueYearCalculator import uniqueYearCalculator

#django
from django_plotly_dash import DjangoDash

df = pd.read_csv('Django_Dash_app/dashplotly/csv/main_database_in_progress.csv')

app_name = "application"
app = DjangoDash('Dashboard')
                #serve_locally=True)
                #app_name=app_name
                #)

# Load styles
#css_url = 'https://codepen.io/IvanNieto/pen/bRPJyb.css'
css_url = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True

#css_url='https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
css_bootstrap_url = 'https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'

app_css_static = '/static/css/app.css'
app.css.append_css({
    "external_url": [css_bootstrap_url,css_url,app_css_static],
})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# for date-Slider
uniqueYear = uniqueYearCalculator(df)
yearDict = {}
keys = range(len(uniqueYear))
for i in keys:
    yearDict[i] = uniqueYear[i]

# for Radioitems
uniqueType = set()
for type in df['Type'].unique():
    uniqueType.add(str(type))
uniqueType = sorted(uniqueType)
uniqueType.remove('nan')

RadioItems_options=[]
for type in uniqueType:
    option={}
    option['label']=str(type)
    option['value']=str(type)
    RadioItems_options.append(option)
select_all = {'label':"Show all types",'value':"All"}
RadioItems_options.append(select_all)
# print("RadioItems_options \n", RadioItems_options)


# for map
mapbox_access_token ="pk.eyJ1Ijoic2Z4aWEiLCJhIjoiY2p0eXFmbXhkMThwczN5cnpoY3V2NXM2OSJ9.y1v1n6o9IQ8q-7xiYE6zNw"

# for timeline
cleanDate = pd.to_datetime(df['Date'], errors='coerce')
df.loc[:, 'Month'] = cleanDate.dt.month
df.loc[:, 'Year'] = cleanDate.dt.year

alert=""

<<<<<<< HEAD
=======

>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
# Layout
app.layout = html.Div(children=[
    html.Div(
        className='container-fluid',
        children=[
            html.Div(
                className='row',
<<<<<<< HEAD
=======
                children=[
                    html.Div(
                        # Radioitems
                        className='col-sm-4',
                        children=[
                            dcc.RadioItems(
                                id="RadioItems",
                                labelClassName="Select Type",
                                options=RadioItems_options,
                                value="",
                                labelStyle={'display': 'inline-block',
                                            'margin': '6px',
                                           },
                            )
                        ],
                        style={
                            'padding':'30px',
                        }
                    ),

                    html.Div(
                        # map
                        className='col-sm-8',
                        children=[
                            dcc.Graph(
                                id="map",
                                config={
                                    'scrollZoom': True
                                },
                            ),
                        ]
                    ),
                ]
            ),

            html.Div(
                # Slider
                className='container',
>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
                children=[
                    html.Div(
                        # Radioitems
                        className='col-sm-4',
                        children=[
                            dcc.RadioItems(
                                id="RadioItems",
                                labelClassName="Select Type",
                                options=RadioItems_options,
                                value="",
                                labelStyle={'display': 'inline-block',
                                            'margin': '6px',
                                           },
                            )
                        ],
                        style={
                            'padding':'10px',
                            'border-style': 'solid',
                            'border-color': '#d7dde5',
                            'background-color': '#f4f6f9',
                            'margin-left':'10px',
                        }
                    ),

                    html.Div(
                        # map
                        className='col-sm-7',
                        children=[

                            dcc.Graph(
                                id="map",
                                config={
                                    'scrollZoom': True
                                },
                            ),
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
                         'margin-bottom':'20px',
                        }
            ),

            html.Div(
                className="container-fuild",
                children=[
                    dcc.Graph(
                        id='timeline',
                    ),
                ],
                style={
                    'margin-bottom':'50px',
<<<<<<< HEAD
                    'width': 'auto',
=======
>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
                }
            ),

            html.Div(
                className='container',
                id='datatable',
                style={
                    'margin-bottom':'100px',
                }
            )
        ]
    ),
])



# map
@app.callback(
    Output('map', 'figure'),
    [Input('slider', 'value'),
    Input('RadioItems','value')])
def update_map(year,type):
    # print("year: ", year)
    # print('type:',type)
    if year == len(uniqueYear):
        newdf = df
    else:
        newdf = df[df.Date.str.contains(str(yearDict[year]), na=False)]

    if (type == "" or type == "All"):
        newdf = newdf
    else:
        newdf =newdf.loc[newdf['Type']==type]

    # print(newdf)
<<<<<<< HEAD
    # nolocation=""



    try:
        coord = newdf['lat,long'].str.split(', ', expand=True)
        newdf.loc[:, 'lat']=coord[0]
        newdf.loc[:, 'long']=coord[1]

    
    except:
        print("some coordinates are mising")

        

    newdf=newdf.fillna('missing')
    nolocationdf=newdf.loc[newdf['lat']=="missing"]
    nolocation=nolocationdf['Name'] 
    print('nolocationdf:', nolocationdf)
    Alert_message=""
    alert='Coordinates for '
    for name in nolocation:
        alert = alert + name+", "
    Alert_message = alert + "are missing."

    print (Alert_message)


    print('newdf:\n', newdf)
=======
    coord = newdf['lat,long'].str.split(', ', expand=True)
    newdf.loc[:, 'lat']=coord[0]
    newdf.loc[:, 'long']=coord[1]

>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
    updated_data = [
        go.Scattermapbox(
            lat=newdf['lat'],
            lon=newdf['long'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=11,
                opacity=0.7,
             ),
            text= df['Name']+"<br>"+newdf['Description'],
        ),
    ]

    layout = dict(
        #autosize= True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            #bearing=0,
            center=dict(lat=-36.85, lon=174.77),
            pitch=0,
            zoom=9,
        ),
<<<<<<< HEAD
        margin = dict(r=40, l=40, t=20, b=20),
        uirevision='same',
        label= Alert_message,
=======
        margin = dict(r=40, l=40, t=40, b=40),
        uirevision='same',
>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
    )

    fig=dict(data=updated_data, layout=layout)

    return fig


# timeline
@app.callback(
    Output('timeline', 'figure'),
    [Input('RadioItems', 'value')])
def update_timeline(type):
    # print ('type: ', type)
    if (type == "" or type == "All"):
        df_timeline = df
    else:
        df_timeline = df[df['Type'] == type]

    print (df_timeline.Type.unique())

    data = [
        go.Scatter(
            x=df_timeline[df_timeline['Type'] == i]['Year'],
            y=df_timeline[df_timeline['Type'] == i]['Month'],
            text=df_timeline[df_timeline['Type'] == i]['Event'],
            mode='markers',
            #textposition='bottom center',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i,
        ) for i in df_timeline.Type.unique()
    ]

    layout = go.Layout(
<<<<<<< HEAD
                autosize=True,
                #width = 1300,
                #height = 300,
=======
                width = 1350,
                height = 300,
>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
                xaxis={ 'title': 'Year',
                        'ticks': '',
                        # 'showticklabels': False,
                      },
                yaxis={'title': 'Month',
                       'showgrid': False,
                       'showline': False,
                       'zeroline': False,
                       'ticks': '',
                       # 'showticklabels': False,
                       },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
<<<<<<< HEAD
                legend={'x': 0, 
                        'y': 1,
                        'orientation':'h'
                        },
                hovermode='closest',
=======
                #legend={'x': 0, 'y': 1},
                hovermode='closest'
>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
            )

    fig=dict(data=data, layout=layout)

    return fig


# DataTable
@app.callback(
    Output('datatable', 'children'),
    [Input('slider', 'value'),
    Input('RadioItems','value')])
def update_table(value,type):
    # print("value:",value)
    if value == len(uniqueYear):
        newdf = df
    else:
        newdf = df[df.Date.str.contains(str(yearDict[value]), na=False)]

    #newdf=pd.DataFrame()

    if (type == "" or type == "All"):
        newdf = newdf
    else:
        #newdf = newdf.append(newdf.loc[newdf['Type']==type])
        newdf=newdf.loc[newdf['Type']==type]

<<<<<<< HEAD
    newdf=newdf.fillna('missing')

=======
>>>>>>> 70115db8aa5d8e19334404d39e19187502042a66
    table = dash_table.DataTable(
        id='table',
        data=newdf.to_dict("rows"),
        columns=[{"name": i, "id": i} for i in newdf.columns \
            if i not in ["Tags", "Image", "Column", "lat,long", "Year", "Month", "lat", "long"]],
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


"""
if __name__ == '__main__':
    app.run_server(debug=True)

"""
