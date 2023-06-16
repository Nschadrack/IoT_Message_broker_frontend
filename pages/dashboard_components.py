import dash
from dash import html, dcc, Input, Output, State
import requests
from flask import json


def generate_dashboard_components(data, app, URL, response_data):
    dashboard = html.Div(children=[
        html.H2("Test Bench Dashboard", className="h2-title"),
        html.Hr(),
        html.Div(children=[
            html.Div([
                html.H3("Publisher", style={"borderBottom": "1px solid #999999",
                                            "textAlign": "center"}),
                html.Div(children=[
                    html.Label("Number of publishers", className="form-group-label"),
                    dcc.Slider(min=0, max=50, className="form-group-input", id="publishers_num",
                               value=data["publishers_num"])
                ], className="form-group-board form-group"),
                html.Div(children=[
                    html.Label("Message delay interval(seconds)", className="form-group-label"),
                    dcc.Slider(min=0, max=1, className="form-group-input", id="message_delay_interval",
                               value=data["message_delay_interval"])
                ], className="form-group-board form-group"),
                html.Div(children=[
                    html.Label("Number of topic levels", className="form-group-label"),
                    dcc.Slider(min=0, max=100, className="form-group-input", id="publishers_topic_levels_num",
                               value=data["publishers_topic_levels_num"])
                ], className="form-group-board form-group"),
                html.Div(children=[
                    html.Label("Message to publish", className="form-group-label"),
                    dcc.Textarea(placeholder="Enter the message to publish",
                                 className="form-group-input",
                                 id="payload", value=data["payload"])
                ], className="form-group-board form-group"),
            ], className='dashboard-item'),
            html.Div([
                html.Button("Broker", className="broker-div-ball", id="broker_eye"),

                html.Div(children=[
                    html.H4("Messages / sec", style={"textAlign": "center"}),
                    html.Div(children=[
                        html.Label("Received", className="form-group-label"),
                        html.P(response_data["received_messages_in_sec"])
                    ], className="messages"),
                    html.Div(children=[
                        html.Label("Sent", className="form-group-label"),
                        html.P(response_data["sent_messages_in_sec"])
                    ], className="messages", style={"marginLeft": "3%"})
                ], className="messages-recv-sent"),

                html.Div(children=[
                    html.Div(children=[
                        html.Label("CPU Used", className="form-group-label"),
                        html.P(f"{response_data['cpu_used']}%")
                    ], className="system-usage"),
                    html.Div(children=[
                        html.Label("Memory Used", className="form-group-label"),
                        html.P(f"{response_data['memory_used']}MB")
                    ], className="system-usage", style={"marginLeft": "3%"})
                ], className="cpu_memory"),

                html.Div(children=[
                    html.Div(children=[
                        html.Label("Network In", className="form-group-label"),
                        html.P(f"{response_data['network_in']} Kbps")
                    ], className="system-usage"),
                    html.Div(children=[
                        html.Label("Network Out", className="form-group-label"),
                        html.P(f"{response_data['network_out']}Kbps")
                    ], className="system-usage", style={"marginLeft": "3%"})
                ], className="cpu_memory")
            ], className='dashboard-item dashboard-middle-item'),
            html.Div([
                html.H3("Subscriber", style={"borderBottom": "1px solid #999999",
                                             "textAlign": "center"}),
                html.Div(children=[
                    html.Label("Number of subscribers", className="form-group-label"),
                    dcc.Slider(min=0, max=50, className="form-group-input", id="subscribers_num",
                               value=data["subscribers_num"])
                ], className="form-group-board form-group"),
                html.Div(children=[
                    html.Label("Number of topic levels", className="form-group-label"),
                    dcc.Slider(min=0, max=100, className="form-group-input", id="subscribers_topic_levels_num",
                               value=data["subscribers_topic_levels_num"])
                ], className="form-group-board form-group"),
            ], className='dashboard-item'),
        ])
    ], className="dashboard")

    return dashboard
