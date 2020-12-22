import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df1 = pd.read_csv('./LAPS.csv')
df2 = pd.read_csv('./GRID.csv')
df3 = pd.read_csv('./SC.csv')
df3.sort_values(by=['lap'], inplace=True)

df = df1.append(df2, ignore_index=True)
df.sort_values(by=['lap'], inplace=True)

trace_list = []
season_list = df['year'].sort_values().unique()
race_list = df['raceId'].sort_values().unique()
gp_list = df['name'].unique()

tab_style = {
    'backgroundColor': '#aaaaaa'
}

tab_style_act = {
    'backgroundColor': '#fafafa'
}

app.layout = html.Center(html.Div([

    html.Hr(),

    html.H1('F1 Grand Prix Timelapses for seasons 1996-2020 '),

    html.Hr(),

    html.Br(),

    html.Div([

        dcc.Dropdown(
            id='dropdown-1',
            options=[
                {'label': 'Season ' + str(c), 'value': c} for c in season_list
            ],
            value=df['year'].max(),
            style={'textAlign':'left'}
        ),

        html.Br(),

        dcc.Dropdown(
            id='dropdown-2',
            style={'textAlign':'left'},
            options=[
                {'label': df.loc[df['raceId'] == r, 'name'].min() + ' (round ' + str(
                    df.loc[df['raceId'] == r, 'round'].min()) + ')'
                    , 'value': r} for r in race_list
            ],
            placeholder='Choose race...',
            value=df['raceId'].max()
        )],
        style={'width': '40%','verticalAlign':'middle'}),

    html.Br(),

    html.Div(
        id='Div1'
    ),

    html.Br(),

    dcc.Tabs(
        id='tabs_1',
        children=[
            dcc.Tab(label='Positions', value='tab1', style=tab_style, selected_style=tab_style_act),
            dcc.Tab(label='Times', value='tab2', style=tab_style, selected_style=tab_style_act),
            dcc.Tab(label='Static', value='tab3', style=tab_style, selected_style=tab_style_act)
        ],
        value='tab1',
        style={'width': '90%', 'margin-left': '5%'},
    ),

    html.Br(),

    dcc.Loading(
        id='load-1',
        children=[html.Div(
            dcc.Graph(
                id='graph-1'
            ))],
        type='default'),

    html.Hr(),

    html.H3('created by @Mati_Karmalski'),

    html.Hr()

], style={'backgroundColor': '#fafafa'}

))


@app.callback(
    [Output("dropdown-2", "options"),
     Output('dropdown-2', 'value')],
    [Input("dropdown-1", "value")],
)
def update_options(seas):
    df_updated = df.query(f'year == {seas}')

    return [[
        {'label': df_updated.loc[df_updated['raceId'] == r, 'name'].min() + ' (round ' + str(
            df_updated.loc[df_updated['raceId'] == r, 'round'].min()) + ')', 'value': r} for r in
        df_updated['raceId'].sort_values().unique()],
        df_updated['raceId'].max()]


@app.callback(
    Output('Div1', 'children'),
    [Input('dropdown-1', 'value'),
     Input('dropdown-2', 'value')]
)
def update_div(selected1, selected2):
    race_name = df.loc[df['raceId'] == selected2, 'name'].min()
    race_round = df.loc[df['raceId'] == selected2, 'round'].min()
    circuit_name = df.loc[df['raceId'] == selected2, 'Circuit_name'].min()
    location_name = df.loc[df['raceId'] == selected2, 'location'].min()
    country_name = df.loc[df['raceId'] == selected2, 'country'].min()
    date_ofrace = df.loc[df['raceId'] == selected2, 'date'].min()
    dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + date_ofrace - 2).strftime('%Y/%m/%d')
    return f'Season {selected1} round {race_round}, {dt} : {race_name} at {circuit_name} ({location_name}, {country_name})'


@app.callback(
    Output('graph-1', 'figure'),

    [Input('tabs_1', 'value'),
     Input('dropdown-2', 'value'),
     Input('dropdown-1', 'value')
     ]
)
def gp_list(typ, race, seas):

    ##POSITION---------------------------------------------------------------------------------------------------


    if typ == 'tab1':
        fig_dict = {
            'data': [],
            'layout': {},
            'frames': [],
            'sliders': []
        }
        lap = 0
        df_updated = df.query(f'year == {seas}')
        df_byrace = df_updated.query(f'raceId == {race}')
        df3_byrace = df3.query(f'raceId == {race}')
        lap_list = df_byrace['lap'].sort_values().unique()
        fig_dict['layout'] = go.Layout(
            xaxis={'showgrid': False,
                   'zeroline': False,
                   'ticks': 'inside',
                   'tickcolor': 'grey',
                   'autorange': False,
                   'range': [-1, lap_list.max() + 7]
                   },
            yaxis={'showgrid': True,
                   'gridcolor': '#1b1b1b',
                   'zeroline': False,
                   'autorange': 'reversed',
                   'ticks': 'inside',
                   'tickcolor': 'darkgrey',
                   'tickvals': [0.5, 5.5, 10.5, 15.5, 20.5],
                   'ticktext': [1, 5, 10, 15, 20]
                   },

            font={'color': 'white'},
            height=800,
            width=1400,
            showlegend=True,
            legend_title_text='Click to show/hide traces',
            plot_bgcolor='#000000',
            paper_bgcolor='#1b1b1b',
            title='F1 Grand Prix Timelapse - Position Changes',
            title_font={'size': 32, 'color': 'white'},
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 500, "redraw": False},
                                            "fromcurrent": True,
                                            "transition": {"duration": 750,
                                                           "easing": "linear"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.1,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top"
                }
            ]
        )

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Lap:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 1000, "easing": "linear"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        ##data start - position changes

        df3_bylap = df3_byrace[df3_byrace['lap'] == lap]
        data_dict0 = go.Scatter(
            x=df3_bylap.lap,
            y=df3_bylap.position,
            mode='markers',
            marker={'line_width': 0, 'size': 8, 'color': 'orange', 'symbol': 'diamond'},
            name=df3_byrace.code.min(),
            showlegend=True
        )

        fig_dict['data'].append(data_dict0)

        driver_list = df_byrace.sort_values(by=['team'])['driverId'].unique()

        for driver in driver_list:
            df_bylap = df_byrace[df_byrace['lap'] == lap]
            df_bylap2 = df_byrace[df_byrace['lap'] <= lap]
            df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
            df_bylap_anddriver2 = df_bylap2[df_bylap2['driverId'] == driver]
            c = df_bylap_anddriver2['team_color'].min()

            data_dict2 = {
                'x': list(df_bylap_anddriver2['lap']),
                'y': list(df_bylap_anddriver2['position']),
                'mode': 'lines',
                'line': {'width': 2, 'color': c, 'dash': df_bylap_anddriver2['line_type'].min()},
                'name': df_bylap_anddriver2['code'].min(),
                'hovertemplate': str(df_bylap_anddriver2.driver.min()) + ' (' + str(
                    df_bylap_anddriver2.team.min()) + ')' +
                                 '<br>Lap: %{x}' +
                                 '<br>Positon: %{y}'
            }
            fig_dict['data'].append(data_dict2)
            data_dict = {
                'x': list(df_bylap_anddriver['lap']),
                'y': list(df_bylap_anddriver['position']),
                'mode': 'markers+text',
                'name': df_bylap_anddriver['code'].min(),
                'text': df_bylap_anddriver['code'].min(),
                'textposition': 'middle right',
                'marker': {'color': c, 'size': 8},
                'showlegend': False,
                'hovertemplate': str(df_bylap_anddriver2.driver.min()) + ' (' + str(
                    df_bylap_anddriver2.team.min()) + ')' +
                                 '<br>Lap: %{x}' +
                                 '<br>Positon: %{y}'
            }
            fig_dict['data'].append(data_dict)


        ##frames- position changes

        for lap in lap_list:

            frame = {'data': [], 'name': str(lap)}

            df3_bylap = df3_byrace[df3_byrace['lap'] <= lap]
            data_dict0 = {
                'x': list(df3_bylap['lap']),
                'y': list(df3_bylap['position']),
                'mode': 'markers',
                'showlegend': True
            }
            frame['data'].append(data_dict0)

            for driver in driver_list:
                df_bylap = df_byrace[df_byrace['lap'] == lap]
                df_bylap2 = df_byrace[df_byrace['lap'] <= lap]
                df_bylap3 = df_byrace[df_byrace['lap'] == lap + 1]
                df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
                df_bylap_anddriver2 = df_bylap2[df_bylap2['driverId'] == driver]
                df_bylap_anddriver3 = df_bylap3[df_bylap3['driverId'] == driver]
                data_dict2 = {
                    'x': list(df_bylap_anddriver2['lap']),
                    'y': list(df_bylap_anddriver2['position']),
                    'mode': 'lines',
                    'name': df_bylap_anddriver2['code'].min(),
                    'text': df_bylap_anddriver2['code'].min(),
                    'textposition': 'middle right'

                }
                frame['data'].append(data_dict2)

                if str(df_bylap_anddriver3['driver'].max()) == 'nan' and \
                        str(df_bylap_anddriver['result'].max()) == 'OUT':
                    pos = list([30])

                else:
                    pos = list(df_bylap_anddriver['position'])

                data_dict = {
                    'x': list(df_bylap_anddriver['lap']),
                    'y': pos,
                    'mode': 'markers+text',
                    'name': df_bylap_anddriver['code'].min(),
                    'text': str(df_bylap_anddriver['code'].min()) + ' +' + str(
                        round(df_bylap_anddriver['strata'].min(), 1)),
                    'textposition': 'middle right'
                }
                frame['data'].append(data_dict)






            fig_dict["frames"].append(frame)
            slider_step = {"args": [
                [lap],
                {"frame": {"duration": 300, "redraw": False},
                 "mode": "immediate",
                 "transition": {"duration": 300}}
            ],
                "label": str(lap),
                "method": "animate"}
            sliders_dict["steps"].append(slider_step)

        fig_dict["layout"]["sliders"] = [sliders_dict]

        return go.Figure(fig_dict)


    ##TIME---------------------------------------------------------------------------------------------------

    elif typ == 'tab2':

        fig_dict = {
            'data': [],
            'layout': {},
            'frames': [],
            'sliders': []
        }

        lap = 0

        df_updated = df.query(f'year == {seas}')
        df_byrace = df_updated.query(f'raceId == {race}')
        df3_byrace = df3.query(f'raceId == {race}')
        lap_list = df_byrace['lap'].sort_values().unique()
        avg_lap_time = df_byrace['seconds'].mean()
        fig_dict['layout'] = go.Layout(
            xaxis={'showgrid': True,
                   'gridcolor': '#1b1b1b',
                   'zerolinecolor': '#1b1b1b',
                   'ticks': 'inside',
                   'tickcolor': '#1b1b1b',
                   'range': [avg_lap_time*2.1, -20],
                   'tickvals': [0, avg_lap_time,avg_lap_time*2,avg_lap_time*2.1],
                   'ticktext': [0,'+'+str(int(avg_lap_time))+'s (~+1LAP)','+'+str(int(2*avg_lap_time))+'s (~+2LAPs)',' ']
                   },
            yaxis={'showgrid': True,
                   'gridcolor': '#1b1b1b',
                   'zeroline': False,
                   'autorange': 'reversed',
                   'ticks': 'inside',
                   'tickcolor': '#1b1b1b',
                   'tickvals': [0.5, 5.5, 10.5, 15.5, 20.5],
                   'ticktext': [1, 5, 10, 15, 20]
                   },

            font={'color': 'white'},
            height=800,
            width=1400,
            showlegend=True,
            legend_title_text='Click to show/hide traces',
            plot_bgcolor='#000000',
            paper_bgcolor='#1b1b1b',
            title='F1 Grand Prix Timelapse - Time Changes',
            title_font={'size': 32, 'color': 'white'},
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 750, "redraw": False},
                                            "fromcurrent": True,
                                            "transition": {"duration": 750,
                                                           "easing": "linear"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.1,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top"
                }
            ]
        )

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Lap:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 1000, "easing": "linear"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        ##data start - TIME changes

        df3_bylap = df3_byrace[df3_byrace['lap'] == lap]

        data_dict0 = go.Scatter(
            x=df3_bylap.strata,
            y=df3_bylap.position,
            mode='markers',
            marker={'line_width': 0, 'size': 8, 'color': 'orange', 'symbol': 'diamond'},
            name=df3_byrace.code.min(),
            showlegend=True
        )

        fig_dict['data'].append(data_dict0)

        driver_list = df_byrace.sort_values(by=['team'])['driverId'].unique()

        for driver in driver_list:

            df_bylap = df_byrace[df_byrace['lap'] == lap]
            df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
            c = df_bylap_anddriver['team_color'].min()

            if str(df_bylap_anddriver['driver'].max()) == 'nan' and \
                    str(df_bylap_anddriver['result'].max()) == 'OUT':
                pos = list([30])

            else:
                pos = list(df_bylap_anddriver['position'])

            data_dict = {
                'x': list(df_bylap_anddriver['strata']),
                'y': pos,
                'mode': 'markers+text',
                'name': df_bylap_anddriver['code'].min(),
                'text': df_bylap_anddriver['code'].min(),
                'textposition': 'middle left',
                'marker': {'color': c, 'size': 10},
                'showlegend': True,
                'hovertemplate': str(df_bylap_anddriver.driver.min()) + ' (' + str(
                    df_bylap_anddriver.team.min()) + ')' +
                                 '<br>Lap: %{x}' +
                                 '<br>Positon: %{y}'
            }
            fig_dict['data'].append(data_dict)

        ##frames- TIME changes

        for lap in lap_list:

            frame = {'data': [], 'name': str(lap)}

            df3_bylap = df3_byrace[df3_byrace['lap'] == lap]
            df3_bylap1 = df3_byrace[df3_byrace['lap'] == lap + 1]

            if str(df3_bylap1['driver'].max()) == 'nan':
                pos2 = list([-2])

            else:
                pos2 = list(df3_bylap['position'])

            data_dict0 = {
                'x': list(df3_bylap['strata']),
                'y': pos2,
                'mode': 'markers+text',
                'showlegend': True
            }
            frame['data'].append(data_dict0)

            for driver in driver_list:
                df_bylap = df_byrace[df_byrace['lap'] == lap]
                df_bylap1 = df_byrace[df_byrace['lap'] == lap + 1]
                df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
                df_bylap_anddriver1 = df_bylap1[df_bylap1['driverId'] == driver]

                if str(df_bylap_anddriver1['driver'].max()) == 'nan' and \
                        str(df_bylap_anddriver['result'].max()) == 'OUT':
                    pos = list([30])

                else:
                    pos = list(df_bylap_anddriver['position'])

                data_dict = {
                    'x': list(df_bylap_anddriver['strata']),
                    'y': pos,
                    'mode': 'markers+text',
                    'name': df_bylap_anddriver['code'].min(),
                    'text': str(df_bylap_anddriver['code'].min()) + ' +' + str(
                        round(df_bylap_anddriver['strata'].min(), 1)),
                    'textposition': 'middle left'
                }

                frame['data'].append(data_dict)

            fig_dict["frames"].append(frame)

            slider_step = {
                "args": [
                    [lap],
                    {"frame": {"duration": 300, "redraw": False},
                     "mode": "immediate",
                     "transition": {"duration": 300}}
                ],
                "label": str(lap),
                "method": "animate"
            }

            sliders_dict["steps"].append(slider_step)

            fig_dict["layout"]["sliders"] = [sliders_dict]

        return go.Figure(fig_dict)

    ##STATIC------------------------------------------------------------------------------

    elif typ == 'tab3':

        fig_dict3 = {
            'data': [],
            'layout': {},
            'frames': []
        }

        df_updated = df.query(f'year == {seas}')
        df_byrace = df_updated.query(f'raceId == {race}')
        df3_byrace = df3.query(f'raceId == {race}')
        driver_list = df_byrace.sort_values(by=['team'])['driverId'].unique()
        lap_list = df_byrace['lap'].sort_values().unique()

    fig_dict3['layout'] = go.Layout(
        xaxis={'showgrid': False,
               'zeroline': False,
               'ticks': 'inside',
               'tickcolor': 'white',
               'range': [-3, lap_list.max() + 7]},
        yaxis={'showgrid': False,
               'zeroline': False,
               'autorange': 'reversed',
               'ticks': 'inside',
               'tickcolor': 'white',
               'tickvals': [1, 5, 10, 15, 20]},
        font={'color': 'white'},
        height=800,
        width=1400,
        showlegend=True,
        plot_bgcolor='#000000',
        paper_bgcolor='#1b1b1b',
        title='F1 Grand Prix Timelapse - Static',
        title_font={'size': 32,
                    'color': 'white'})

    z = -1

    trace0 = go.Scatter(
        x=df3_byrace.lap,
        y=df3_byrace.position,
        mode='markers',
        name=df3_byrace.code.min(),
        line={'width': 2, 'dash': df3_byrace['line_type'].min()},
        marker={'line_width': 0, 'size': 8, 'color': 'orange', 'symbol': 'diamond'},
        textposition='middle right',

    )
    fig_dict3['data'].append(trace0)

    for i in driver_list:
        z = z + 1
        df_trace = df_byrace[df_byrace['driverId'] == i]
        c = df_trace['team_color'].min()
        driver_lap_max = df_trace['lap'].max()
        trace = go.Scatter(
            x=df_trace.lap,
            y=df_trace.position,
            mode='lines',
            name=df_trace.code.min(),
            line={'width': 2, 'dash': df_trace['line_type'].min()},
            marker={'line_width': 0, 'size': 8, 'color': c},
            text=df_trace.code.min(),
            textposition='middle right',
            hovertemplate=
            df_trace.driver.min() + ' (' + df_trace.team.min() + ')' +
            '<br>Lap: %{x}' +
            '<br>Positon: %{y}'

        )
        fig_dict3['data'].append(trace)

        df_trace2 = df_trace[df_trace['lap'] == 0]

        trace2 = go.Scatter(
            x=df_trace2.lap,
            y=df_trace2.position,
            mode='markers+text',
            name=df_trace2.code.min(),
            marker={'line_width': 0, 'size': 8, 'color': c},
            text=df_trace2.code.min(),
            textposition='middle left',
            showlegend=False,
            hovertemplate=
            str(df_trace2.driver.min()) + ' (' + str(df_trace2.team.min()) + ')' +
            '<br>Lap: %{x}' +
            '<br>Positon: %{y}'

        )
        fig_dict3['data'].append(trace2)

        df_trace3 = df_trace[df_trace['lap'] == driver_lap_max]

        trace3 = go.Scatter(
            x=df_trace3.lap,
            y=df_trace3.position,
            mode='markers',
            name=df_trace3.code.min(),
            marker={'line_width': 0, 'size': 8, 'color': c},

            textposition='middle right',
            showlegend=False,
            hovertemplate=
            str(df_trace3.driver.min()) + ' (' + str(df_trace3.team.min()) + ')' +
            '<br>Lap: %{x}' +
            '<br>Positon: %{y}'

        )
        fig_dict3['data'].append(trace3)

        df_trace4 = df_trace3[df_trace3['result'] == 'CLASS']

        trace4 = go.Scatter(
            x=df_trace4.lap,
            y=df_trace4.position,
            mode='text',
            name=df_trace4.code.min(),
            marker={'line_width': 0, 'size': 8, 'color': c},
            text='  '+str(df_trace4.code.min()) + ' +' + str(round(df_trace4['strata'].min(), 1)),
            textposition='middle right',
            showlegend=False,
            hovertemplate=
            str(df_trace4.driver.min()) + ' (' + str(df_trace4.team.min()) + ')' +
            '<br>Lap: %{x}' +
            '<br>Positon: %{y}'

        )
        fig_dict3['data'].append(trace4)

    return go.Figure(fig_dict3)


##df_gp = df[df['year'] == season]
##race_list = df_gp['raceId'].sort_values().unique()
##return [{'label': r, 'value': r} for r in race_list]


if __name__ == '__main__':
    app.run_server(debug=True)
