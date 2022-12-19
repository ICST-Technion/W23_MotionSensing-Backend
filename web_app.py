import numpy as np
import collections
import pandas as pd
import threading
import time
from dash import Dash, dcc, html, Input, Output, callback_context
import plotly
import plotly.express as px
import plotly.graph_objects as go
from imus_handler import ImusHandler

#############################
app = Dash(__name__)
imus = None
#############################


#############################
def thread_function(imus: ImusHandler):
    while True:
        imus.read_data()
        time.sleep(0.0001)
#############################


class WebAPP:
    def __init__(self, imus_in: ImusHandler):
        global imus
        imus = imus_in
        self.imus = imus_in

    def get_layout(self):
        layout = html.Div(className="container", children=[
                                html.H1(className="header", children="IMU's Raw Data"),
                                html.Div(className="main-container", children=[     # holds IMU enable and figure enable divs
                                            html.H2(className="container-header", children="Control"),
                                            html.Div(style={'display': 'flex'}, children=[
                                                        html.Div(id="imus-enable-div", children=[
                                                                    html.H3(className="inner-container-header", children='Enable IMUs'),
                                                                    dcc.Checklist(id="imus-control-checklist", className="checklist-style",
                                                                                    options=[{"label": f'{imu_obj.name}-{imu_obj.mac_address}', "value": imu_obj.name} for imu_obj in self.imus.imus_obj.values()],
                                                                                    value=[imu_obj.name for imu_obj in list(self.imus.imus_obj.values())[:1]],
                                                                                    labelStyle={"display": "flex"})]  # also in css
                                                                 ),
                                                        html.Div(id="figures-enable-div", children=[
                                                            html.H3(className="inner-container-header", children='Enable figures'),
                                                            html.Div(style={'display': 'flex', 'flex-direction': 'row'}, children=[
                                                                        dcc.Checklist(id="plot-control-checklist", className="checklist-style",
                                                                                        options=[
                                                                                            {"label": "Acceleration", "value": "ACC"},
                                                                                            {"label": "Gyro", "value": "GYRO"},
                                                                                            {"label": "Roll, Pitch, Yaw", "value": "Angle"}],
                                                                                        value=["ACC"], #, "GYRO", "Angle"
                                                                                      ),
                                                                        dcc.Checklist(id="plot-axis-control-checklist", className="checklist-style",
                                                                                        options=[
                                                                                            {"label": "X", "value": "X"},
                                                                                            {"label": "Y", "value": "Y"},
                                                                                            {"label": "Z", "value": "Z"}],
                                                                                        value=["X", "Y", "Z"],
                                                                                      )]
                                                            )
                                                        ])
                                            ]),
                                ]),

                                # Data section
                                html.Div(className="main-container", children=[
                                            html.H2(className="container-header", children='Data'),
                                            # X-axis container
                                            html.Div(className="sub-plot-container", children=[
                                                        html.Div(id="Acc-X-div", children=[
                                                                    dcc.Graph(id='ACC-X-figure'),
                                                                ]),
                                                        html.Div(id="Gyro-X-div", children=[
                                                                dcc.Graph(id='GYRO-X-figure'),
                                                                ]),
                                                        html.Div(id="Angle-X-div", children=[
                                                                dcc.Graph(id='Angle-X-figure'),
                                                                ]),
                                            ]),
                                            # Y-axis container
                                            html.Div(className="sub-plot-container", children=[
                                                        html.Div(id="Acc-Y-div", children=[
                                                                    dcc.Graph(id='ACC-Y-figure'),
                                                                ]),
                                                        html.Div(id="Gyro-Y-div", children=[
                                                                dcc.Graph(id='GYRO-Y-figure'),
                                                                ]),
                                                        html.Div(id="Angle-Y-div", children=[
                                                                dcc.Graph(id='Angle-Y-figure'),
                                                                ]),
                                            ]),
                                            # Y-axis container
                                            html.Div(className="sub-plot-container", children=[
                                                        html.Div(id="Acc-Z-div", children=[
                                                                    dcc.Graph(id='ACC-Z-figure'),
                                                                ]),
                                                        html.Div(id="Gyro-Z-div", children=[
                                                                dcc.Graph(id='GYRO-Z-figure'),
                                                                ]),
                                                        html.Div(id="Angle-Z-div", children=[
                                                                dcc.Graph(id='Angle-Z-figure'),
                                                                ]),
                                            ]),
                                ]),

                            # dcc.Graph(id='live-update-graph'),
                            dcc.Interval(id='interval-component',
                                      interval=1*100,  # in milliseconds
                                      n_intervals=0),
        ])
        return layout

    def run_app(self):
        x = threading.Thread(target=thread_function, args=(self.imus,))
        x.start()
        app.run_server(debug=True)


@app.callback(Output(component_id='Acc-X-div', component_property='style'),
              Output(component_id='Gyro-X-div', component_property='style'),
              Output(component_id='Angle-X-div', component_property='style'),
              Output(component_id='Acc-Y-div', component_property='style'),
              Output(component_id='Gyro-Y-div', component_property='style'),
              Output(component_id='Angle-Y-div', component_property='style'),
              Output(component_id='Acc-Z-div', component_property='style'),
              Output(component_id='Gyro-Z-div', component_property='style'),
              Output(component_id='Angle-Z-div', component_property='style'),
              Input(component_id='plot-control-checklist', component_property='value'),
              Input(component_id='plot-axis-control-checklist', component_property='value'))
def enable_plot_div(plot_type, axis2plot):

    num_of_rows = len(plot_type)
    num_of_cols = len(axis2plot)

    style = {"width": f'{100 / num_of_cols - 2}%',
             "margin-right": "10px",
             # "height": "150px",
             "box-shadow": "rgb(0 0 0 / 25%) 0px 0.0625em 0.0625em, rgb(0 0 0 / 25%) 0px 0.125em 0.5em, rgb(255 255 255 / 10%) 0px 0px 0px 1px inset",
             "border-radius": "10px",
             "padding": "5px"}

    style_list = [[{'display': 'none'}, {'display': 'none'}, {'display': 'none'}],
                  [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}],
                  [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}]]

    for i, pl_type in enumerate(['ACC', 'GYRO', 'Angle']):
        for j, axis_type in enumerate(['X', 'Y', 'Z']):

            if (pl_type in plot_type) and (axis_type in axis2plot):
                style_list[i][j] = style

    out_list = style_list[0] + style_list[1] + style_list[2]

    return out_list


@app.callback(Output(component_id='ACC-X-figure', component_property='figure'),
              Output(component_id='GYRO-X-figure', component_property='figure'),
              Output(component_id='Angle-X-figure', component_property='figure'),
              Output(component_id='ACC-Y-figure', component_property='figure'),
              Output(component_id='GYRO-Y-figure', component_property='figure'),
              Output(component_id='Angle-Y-figure', component_property='figure'),
              Output(component_id='ACC-Z-figure', component_property='figure'),
              Output(component_id='GYRO-Z-figure', component_property='figure'),
              Output(component_id='Angle-Z-figure', component_property='figure'),

              Input(component_id='interval-component', component_property='n_intervals'),  # interval
              Input(component_id='imus-control-checklist', component_property='value'),  # enabled IMUs
              Input(component_id='plot-control-checklist', component_property='value'),
              # plot control ["ACC", "GYRO", "Angle"]
              Input(component_id='plot-axis-control-checklist', component_property='value'))  # plot axis ["X", "Y", "Z"]
def update_graph_live(n, imus_list, plot_type, axis2plot):
    global imus
    figs_name_list = [{}]*9
    for i, pt in enumerate(plot_type):  # ['ACC', 'GYRO', 'Angle']
        for j, ax in enumerate(axis2plot):  # ['X', 'Y', 'Z']
            fig_name = f'{pt}-{ax}'
            title = fig_name
            if pt == 'Angle':
                if ax == 'X':
                    title = 'roll'
                elif ax == 'Y':
                    title = 'pitch'
                else:
                    title = 'yaw'

            fig = go.Figure()
            for imu_name in imus_list:  # ['IMU-0', 'IMU-1']
                y = imus.imus_obj[imu_name].imu_data[fig_name]
                x = np.arange(len(y))
                fig.add_trace({
                    'x': x,
                    'y': np.array(y),
                    'name': imu_name,
                    'mode': 'lines+markers',
                    'line_color': imus.imus_obj[imu_name].color,
                    'legendgroup': 'group1',
                    # 'showlegend': ((imu_idx == 1) and (data_type_idx == 1)),
                    'type': 'scatter'})
            fig.update_layout(title=title, xaxis_title="time step")
            figs_name_list[i*3 + j] = fig

    return figs_name_list