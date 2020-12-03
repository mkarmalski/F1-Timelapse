import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./Races.csv')

driver_list = []
driver_list = df['Driver Code'].unique()
lap_list = []
lap_list = df['lap'].unique()
trace_list = []
colors_list = ['#FD3216', '#00FE35', '#6A76FC', '#FED4C4', '#FE00CE', '#0DF9FF', '#F6F926',
               '#FF9616', '#479B55', '#EEA6FB', '#DC587D', '#D626FF', '#6E899C', '#00B5F7',
               '#B68E00', '#C9FBE5', '#FF0092', '#22FFA7', '#E3EE9E', '#86CE00', '#BC7196',
               '#7E7DCD', '#FC6955', '#E48F72']

##POSITION CHANGES------------------------------------------------------------------------------------
fig_dict = {
    'data': [],
    'layout': {},
    'frames': []
}

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
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True,
                                    "transition": {"duration": 500,
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
for driver in driver_list:
    i = i + 1
    c = colors_list[i]
    df_bylap = df[df['lap'] == lap]
    df_bylap2 = df[df['lap'] <= lap]
    df_bylap_anddriver = df_bylap[df_bylap['Driver Code'] == driver]
    df_bylap_anddriver2 = df_bylap2[df_bylap2['Driver Code'] == driver]
    data_dict2 = {
        'x': list(df_bylap_anddriver2['lap']),
        'y': list(df_bylap_anddriver2['position']),
        'mode': 'lines',
        'line': {'width': 3, 'color': c},
        'name': driver
    }
    fig_dict['data'].append(data_dict2)
    data_dict = {
        'x': list(df_bylap_anddriver['lap']),
        'y': list(df_bylap_anddriver['position']),
        'mode': 'markers+text',
        'name': driver,
        'text': driver,
        'textposition': 'middle right',
        'marker': {'color': c, 'size': 10},
        'showlegend': False
    }
    fig_dict['data'].append(data_dict)

##frames- position changes

for lap in lap_list:
    frame = {'data': [], 'name': str(lap)}
    for driver in driver_list:
        df_bylap = df[df['lap'] == lap]
        df_bylap2 = df[df['lap'] <= lap]
        df_bylap_anddriver = df_bylap[df_bylap['Driver Code'] == driver]
        df_bylap_anddriver2 = df_bylap2[df_bylap2['Driver Code'] == driver]
        data_dict2 = {
            'x': list(df_bylap_anddriver2['lap']),
            'y': list(df_bylap_anddriver2['position']),
            'mode': 'lines',
            'name': driver,
            'text': driver,
            'textposition': 'middle right'
        }
        frame['data'].append(data_dict2)
        data_dict = {
            'x': list(df_bylap_anddriver['lap']),
            'y': list(df_bylap_anddriver['position']),
            'mode': 'markers+text',
            'name': driver,
            'text': driver,
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

##static wykres---------------------------------------------------------------------------------------
z = -1
for i in driver_list:
    z = z + 1
    df_trace = df[df['Driver Code'] == i]
    trace = go.Scatter(
        x=df_trace.lap,
        y=df_trace.position,
        mode='markers+lines',
        name=i,
        marker={'line_width': 0, 'size': 5, 'color': colors_list[z]},
        text=i,
        textposition='middle right'

    )
    trace_list.append(trace)

##TIME CHANGES----------------------------------------------------------

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
           'range':[-500,100]
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
    df_bylap_anddriver = df_bylap[df_bylap['Driver Code'] == driver]
    data_dict = {
        'x': list(df_bylap_anddriver['Strata']),
        'y': list(df_bylap_anddriver['position']),
        'mode': 'markers+text',
        'name': driver,
        'text': driver,
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
        df_bylap_anddriver = df_bylap[df_bylap['Driver Code'] == driver]
        st_zaw = df_bylap_anddriver['Strata'].min()
        data_dict = {
            'x': list(df_bylap_anddriver['Strata']),
            'y': list(df_bylap_anddriver['position']),
            'mode': 'markers+text',
            'name': driver,
            'text': driver + str('  ') + str(round(st_zaw, 3)),
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




app.layout = html.Center(html.Div([

    html.Hr(),



    dcc.Graph(
        figure=go.Figure(fig_dict2),
      ),
    html.Hr(),

    dcc.Graph(
        figure=go.Figure(fig_dict)),
    html.Hr(),
    dcc.Graph(
        figure=go.Figure(
            data=trace_list,
            layout=go.Layout(
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
                title_font={'size': 32, 'color': 'white'},

            )

        )
    ),
    html.Hr()
]))

if __name__ == '__main__':
    app.run_server(debug=True)
