import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df1 = pd.read_csv('./LAPS.csv')
df2 = pd.read_csv('./GRID.csv')
df = df1.append(df2, ignore_index=True)
df.sort_values(by=['lap'], inplace=True)
##df = df.query('raceId >= 1000')


trace_list = []
colors_list = ['#FD3216', '#00FE35', '#6A76FC', '#FED4C4', '#FE00CE', '#0DF9FF', '#F6F926',
               '#FF9616', '#479B55', '#EEA6FB', '#DC587D', '#D626FF', '#6E899C', '#00B5F7',
               '#B68E00', '#C9FBE5', '#FF0092', '#22FFA7', '#E3EE9E', '#86CE00', '#BC7196',
               '#7E7DCD', '#FC6955', '#E48F72', '#FD3216', '#00FE35', '#6A76FC', '#FED4C4', '#FE00CE', '#0DF9FF',
               '#F6F926',
               '#FF9616', '#479B55', '#EEA6FB', '#DC587D', '#D626FF', '#6E899C', '#00B5F7',
               '#B68E00', '#C9FBE5', '#FF0092', '#22FFA7', '#E3EE9E', '#86CE00', '#BC7196',
               '#7E7DCD', '#FC6955', '#E48F72', '#FD3216', '#00FE35', '#6A76FC', '#FED4C4', '#FE00CE', '#0DF9FF',
               '#F6F926',
               '#FF9616', '#479B55', '#EEA6FB', '#DC587D', '#D626FF', '#6E899C', '#00B5F7',
               '#B68E00', '#C9FBE5', '#FF0092', '#22FFA7', '#E3EE9E', '#86CE00', '#BC7196',
               '#7E7DCD', '#FC6955', '#E48F72']
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

    dcc.Dropdown(
        id='dropdown-1',
        options=[
            {'label': 'Season ' + str(c), 'value': c} for c in season_list
        ],
        value=df['year'].max(),
        style={'width': '60%'}
    ),

    html.Br(),

    dcc.Dropdown(
        id='dropdown-2',
        style={'width': '60%'},
        options=[
            {'label': df.loc[df['raceId'] == r, 'name'].min() + ' (round ' + str(
                df.loc[df['raceId'] == r, 'round'].min()) + ')'
                , 'value': r} for r in race_list
        ],
        placeholder='Choose race...',
        value=df['raceId'].max()
    ),

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
            style={'width': '90%','margin-left':'5%'},
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
    if not seas:
        raise PreventUpdate
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
            'frames': []
        }
        df_updated = df.query(f'year == {seas}')
        df_byrace = df_updated.query(f'raceId == {race}')
        lap_list = []
        lap_list = df_byrace['lap'].unique()
        fig_dict['layout'] = go.Layout(
            xaxis={'showgrid': False,
                   'zeroline': False,
                   'ticks': 'inside',
                   'tickcolor': 'grey',
                   'autorange': False,
                   'range': [-1, lap_list.max() + 3]
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

        ##data start - position changes
        lap = 0
        i = -1

        driver_list = df_byrace['driverId'].unique()
        for driver in driver_list:
            i = i + 1
            c = colors_list[i]
            df_bylap = df_byrace[df_byrace['lap'] == lap]
            df_bylap2 = df_byrace[df_byrace['lap'] <= lap]
            df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
            df_bylap_anddriver2 = df_bylap2[df_bylap2['driverId'] == driver]
            data_dict2 = {
                'x': list(df_bylap_anddriver2['lap']),
                'y': list(df_bylap_anddriver2['position']),
                'mode': 'lines',
                'line': {'width': 3, 'color': c},
                'name': df_bylap_anddriver2['code'].min(),
                'hovertemplate': df_bylap_anddriver2.driver.min() + ' (' + df_bylap_anddriver2.team.min() + ')' +
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
                'marker': {'color': c, 'size': 10},
                'showlegend': False,
                'hovertemplate': df_bylap_anddriver2.driver.min() + ' (' + df_bylap_anddriver2.team.min() + ')' +
                                 '<br>Lap: %{x}' +
                                 '<br>Positon: %{y}'
            }
            fig_dict['data'].append(data_dict)

        ##frames- position changes

        for lap in lap_list:
            frame = {'data': [], 'name': str(lap)}
            driver_list = df_byrace['driverId'].unique()
            for driver in driver_list:
                df_bylap = df_byrace[df_byrace['lap'] == lap]
                df_bylap2 = df_byrace[df_byrace['lap'] <= lap]
                df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
                df_bylap_anddriver2 = df_bylap2[df_bylap2['driverId'] == driver]
                data_dict2 = {
                    'x': list(df_bylap_anddriver2['lap']),
                    'y': list(df_bylap_anddriver2['position']),
                    'mode': 'lines',
                    'name': df_bylap_anddriver2['code'].min(),
                    'text': df_bylap_anddriver2['code'].min(),
                    'textposition': 'middle right'

                }
                frame['data'].append(data_dict2)
                data_dict = {
                    'x': list(df_bylap_anddriver['lap']),
                    'y': list(df_bylap_anddriver['position']),
                    'mode': 'markers+text',
                    'name': df_bylap_anddriver['code'].min(),
                    'text': df_bylap_anddriver['code'].min(),
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
        fig_dict2 = {
            'data': [],
            'layout': {},
            'frames': []
        }

        fig_dict2['layout'] = go.Layout(
            xaxis={'showgrid': False,
                   'zeroline': False,
                   'ticks': 'inside',
                   'tickcolor': 'grey',
                   'range': [-500, 100]
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
            title='F1 Grand Prix Timelapse - Time Changes',
            title_font={'size': 32, 'color': 'white'},
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 1000, "redraw": False},
                                            "fromcurrent": True,
                                            "transition": {"duration": 1000,
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

        sliders_dict2 = {
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

        ##data start - time change
        lap = 0
        i = -1

        for driver in driver_list:
            i = i + 1
            c = colors_list[i]
            df_bylap = df[df['lap'] == lap]
            df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
            data_dict = {
                'x': list(df_bylap_anddriver['strata']),
                'y': list(df_bylap_anddriver['position']),
                'mode': 'markers+text',
                'name': df_bylap_anddriver['code'].min(),
                'text': df_bylap_anddriver['code'].min(),
                'textposition': 'middle right',
                'marker': {'color': c, 'size': 10},
                'showlegend': False
            }
            fig_dict2['data'].append(data_dict)

        ##frames - time changes

        for lap in lap_list:
            frame = {'data': [], 'name': str(lap)}
            ##st_min = df[df['lap'] == lap]['Strata'].min()
            ##frame['layout'] = {'xaxis': {'range': [-100,10]}}
            for driver in driver_list:
                df_bylap = df[df['lap'] == lap]
                df_bylap_anddriver = df_bylap[df_bylap['driverId'] == driver]
                st_zaw = df_bylap_anddriver['strata'].min()
                data_dict = {
                    'x': list(df_bylap_anddriver['strata']),
                    'y': list(df_bylap_anddriver['position']),
                    'mode': 'markers+text',
                    'name': df_bylap_anddriver['code'].min(),
                    'text': str(df_bylap_anddriver['code'].min()) + str('  ') + str(round(st_zaw, 3)),
                    'textposition': 'middle right'
                }
                frame['data'].append(data_dict)

            fig_dict2["frames"].append(frame)

            slider_step2 = {"args": [
                [lap],
                {"frame": {"duration": 300, "redraw": False},
                 "mode": "immediate",
                 "transition": {"duration": 300}}
            ],
                "label": str(lap),
                "method": "animate"}
            sliders_dict2["steps"].append(slider_step2)

        fig_dict2["layout"]["sliders"] = [sliders_dict2]

        return go.Figure(fig_dict2)
    ##STATIC------------------------------------------------------------------------------
    elif typ == 'tab3':

        fig_dict3 = {
            'data': [],
            'layout': {},
            'frames': []
        }

        fig_dict3['layout'] = go.Layout(
            xaxis={'showgrid': False,
                   'zeroline': False,
                   'ticks': 'inside',
                   'tickcolor': 'white'},
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
        df_updated = df.query(f'year == {seas}')
        df_byrace = df_updated.query(f'raceId == {race}')
        driver_list = df_byrace['driverId'].unique()
        for i in driver_list:
            z = z + 1
            df_trace = df_byrace[df_byrace['driverId'] == i]
            trace = go.Scatter(
                x=df_trace.lap,
                y=df_trace.position,
                mode='markers+lines',
                name=df_trace.code.min(),
                marker={'line_width': 0, 'size': 5, 'color': colors_list[z]},
                text=df_trace.code.min(),
                textposition='middle right',
                hovertemplate=
                df_trace.driver.min() + ' (' + df_trace.team.min() + ')' +
                '<br>Lap: %{x}' +
                '<br>Positon: %{y}'

            )
            fig_dict3['data'].append(trace)

        return go.Figure(fig_dict3)

    ##df_gp = df[df['year'] == season]
    ##race_list = df_gp['raceId'].sort_values().unique()
    ##return [{'label': r, 'value': r} for r in race_list]


if __name__ == '__main__':
    app.run_server(debug=True)
