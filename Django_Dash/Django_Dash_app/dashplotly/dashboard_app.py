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

# for Checklist_items
uniqueType = set()
for type in df['Type'].unique():
    uniqueType.add(str(type))
uniqueType = sorted(uniqueType)
uniqueType.remove('nan')

checklist_options=[]
for type in uniqueType:
    option={}
    option['label']=str(type)
    option['value']=str(type)
    checklist_options.append(option)
select_all = {'label':"Show all types",'value':"All"}
checklist_options.append(select_all)


# for map
mapbox_access_token ="pk.eyJ1Ijoic2Z4aWEiLCJhIjoiY2p0eXFmbXhkMThwczN5cnpoY3V2NXM2OSJ9.y1v1n6o9IQ8q-7xiYE6zNw"

# for timeline
cleanDate = pd.to_datetime(df['Date'], errors='coerce')
df.loc[:, 'Month'] = cleanDate.dt.month
df.loc[:, 'Year'] = cleanDate.dt.year

alert=""

# Layout
app.layout = html.Div(children=[
    html.Div(
        className='container-fluid',
        children=[
            html.Div(
                dcc.ConfirmDialog(
                    id='confirm',
                    message='Your selected range has no data! Try again!',
                    displayed=False
                ),
            ),

            html.Div(id='output-confirm'),
            
            html.Div(
                className='row',
                children=[
                    html.Div(
                        # checklist
                        className='col-sm-4',
                        children=[
                            html.Div(
                                className='container-fuild',
                                children=[
                                    dcc.Checklist(
                                        id="checklist",
                                        labelClassName="Select Type",
                                        options=checklist_options,
                                        values=['All'],
                                        labelStyle={'display': 'inline-block',
                                                    'margin': '6px',
                                                   },
                                    )
                                ],
                                style={
                                    'border-style': 'solid',
                                    'border-color': '#d7dde5',
                                    'background-color': '#f4f6f9',
                                    'padding': '5px',
                                }
                            )
                        ]
                    ),

                    html.Div(
                        className='col-sm-8',
                        children=[
                            # map
                            dcc.Graph(
                                id="map",
                                config={
                                    'scrollZoom': True
                                },
                                animate=True,
                            ),
                            # slider
                            dcc.RangeSlider(
                                id='slider',
                                min=0,
                                max=len(uniqueYear),
                                marks={str(k):str(v) for k, v in yearDict.items()},
                                # min=min(uniqueYear),
                                # max=max(uniqueYear),
                                # marks={str(date):str(date) for date in uniqueYear},
                                value=[0,len(uniqueYear)-1],
                            )

                        ],
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
                    'width': 'auto',
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
    Input('checklist','values')])
def update_map(years,types):
    # print("years: ", years)
    # print('types:', types)
    # filter by year
    selected_years = [str(yearDict[x]) for x in range(years[0], years[1])]
    newdf = df.loc[df.Date.str.contains('|'.join(selected_years), na=False)]

    # filter by types
    if 'All' in types:
        pass
    else:
        newdf = newdf.loc[newdf['Type'].isin(types)]

    Alert_message=""
    newdf=newdf.fillna('missing')
    print('newdf:\n', newdf)
    # print(newdf)
    if not newdf.empty:
        try:
            coord = newdf['lat,long'].str.split(', ', expand=True)
            newdf.loc[:, 'lat']=coord[0]
            newdf.loc[:, 'long']=coord[1]

        except:
            print("some coordinates are missing")
        
        """
        nolocationdf=newdf.loc[newdf['lat']=="missing"]
        nolocation=nolocationdf['Name']

        alert='Coordinates for '
        for name in nolocation:
            alert = alert + name+", "
            Alert_message = alert + "are missing."

        print (Alert_message)
        """
        updated_data = [
            go.Scattermapbox(
                lat=newdf[newdf['Type']==i]['lat'],
                lon=newdf[newdf['Type']==i]['long'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=11,
                    opacity=0.7,
                ),
                text=newdf[newdf['Type']==i]['Name']+"<br>"+newdf[newdf['Type']==i]['Description'],
                name=i,
            ) for i in newdf.Type.unique()
        ]


    else:
        newdf = pd.DataFrame()   
        updated_data = [
            go.Scattermapbox(
                lat=[],
                lon=[],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=11,
                    opacity=0.7,
                ),
            ),
        ]

    

    layout = dict(
        autosize= True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(lat=-36.85, lon=174.77),
            pitch=0,
            zoom=10,
        ),
        margin = dict(r=40, l=40, t=20, b=20),
        uirevision='same',
        label= Alert_message,
    )

    fig=dict(data=updated_data, layout=layout)

    return fig


# timeline
@app.callback(
    Output('timeline', 'figure'),
    [Input('slider', 'value'),
    Input('checklist', 'values')])
def update_timeline(years, types):
    # print ('types: ', types)
    #print ('years: ', years)
    # filter by years
    selected_years = [str(yearDict[x]) for x in range(years[0], years[1])]
    df_timeline = df.loc[df.Date.str.contains('|'.join(selected_years), na=False)]

    # filter by types
    if 'All' in types:
        pass
    else:
        df_timeline = df_timeline.loc[df['Type'].isin(types)]


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
                autosize=True,
                #width = 1300,
                #height = 300,
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
                hovermode='closest',
            )

    fig=dict(data=data, layout=layout)

    return fig

# Alert Message
@app.callback(
    Output('confirm', 'displayed'),
    [Input('slider', 'value'),
    Input('checklist', 'values')])

def display_confirm(years, types):
    # filter by years
    selected_years = [str(yearDict[x]) for x in range(years[0], years[1])]
    df_confirm = df.loc[df.Date.str.contains('|'.join(selected_years), na=False)]

    # filter by types
    if 'All' in types:
        pass
    else:
        df_confirm = df_confirm.loc[df['Type'].isin(types)]

    if df_confirm.empty:
        return True
    return False

# prevent reloading confirm dialog
@app.callback(Output('output-confirm', 'children'),
              [Input('confirm', 'submit_n_clicks')])
def update_output(submit_n_clicks):
    if submit_n_clicks:
        return 'It wasnt easy but we did it {}'.format(submit_n_clicks)

# DataTable
@app.callback(
    Output('datatable', 'children'),
    [Input('slider', 'value'),
    Input('checklist','values')])
def update_table(years,types):
    # print("value:",value)
    selected_years = [str(yearDict[x]) for x in range(years[0], years[1])]
    table_df = df.loc[df.Date.str.contains('|'.join(selected_years), na=False)]


    #newdf=pd.DataFrame()

    if 'All' in types:
        pass
    else:
        table_df= table_df.loc[table_df['Type'].isin(types)]

    table_df.fillna('missing')

    table = dash_table.DataTable(
        id='table',
        data=table_df.to_dict("rows"),
        columns=[{"name": i, "id": i} for i in table_df.columns \
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
