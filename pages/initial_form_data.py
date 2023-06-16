import dash
from dash import html, dcc, Input, State, Output
import requests
from flask import json
import time

from pages.dashboard_components import generate_dashboard_components


def generate_initial_form_data(initial_form_required_fields, app, data, URL):
    initial_div_form_data = html.Div(children=[
        html.H2("Initial Data and Settings", className="h2-title"),
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.Label("Username", className="form-group-label"),
                    dcc.Input(type="text", placeholder="Enter username...", required=initial_form_required_fields,
                              className="form-group-input", id="username")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Host", className="form-group-label"),
                    dcc.Input(type="text", placeholder="Enter host...", required=initial_form_required_fields,
                              className="form-group-input", id="host")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Number of publishers", className="form-group-label"),
                    dcc.Input(type="number", placeholder="Enter publishers...",
                              required=initial_form_required_fields,
                              className="form-group-input", id="publishers_num")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Number of topic levels for publishers", className="form-group-label"),
                    dcc.Input(type="number", placeholder="Enter publishers topic levels...",
                              required=initial_form_required_fields,
                              className="form-group-input", id="publishers_topic_levels_num")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Topic level", className="form-group-label"),
                    dcc.Input(type="text", placeholder="Enter topic level...", required=initial_form_required_fields,
                              className="form-group-input", id="topic_level")
                ], className="form-group")
            ], className="div-form-input"),

            html.Div(children=[
                html.Div(children=[
                    html.Label("Password", className="form-group-label"),
                    dcc.Input(type="password", placeholder="Enter password...",
                              required=initial_form_required_fields,
                              className="form-group-input", id="password")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Port", className="form-group-label"),
                    dcc.Input(type="number", placeholder="Enter port...", required=initial_form_required_fields,
                              className="form-group-input", id="port")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Number of subscribers", className="form-group-label"),
                    dcc.Input(type="number", placeholder="Enter subscribers...",
                              required=initial_form_required_fields,
                              className="form-group-input", id="subscribers_num")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Number of topic levels for subscribers", className="form-group-label"),
                    dcc.Input(type="number", placeholder="Enter subscribers topic levels...",
                              required=initial_form_required_fields,
                              className="form-group-input", id="subscribers_topic_levels_num")
                ], className="form-group"),
                html.Div(children=[
                    html.Label("Message delay interval(in seconds, max=2)", className="form-group-label"),
                    dcc.Input(type="number", placeholder="Enter delay interval...",
                              required=initial_form_required_fields,
                              className="form-group-input", id="message_delay_interval", max=2)
                ], className="form-group")
            ], className="div-form-input"),
            html.Div(children=[
                html.Div(children=[
                    html.Label("Message to publish", className="form-group-label"),
                    dcc.Textarea(placeholder="Enter the message to publish",
                                 className="form-group-input",
                                 id="payload-initial", required=initial_form_required_fields),
                ], className="form-group-text-area payload-item"),
                html.Button("Initialize Test", className="payload-item form-group-btn", id="initializing-btn")
            ], className="payload-submit-button form-group")
        ], className="initial-form"),
    ], className="initial-data")

    @app.callback(
        Output(component_id='loading-component', component_property="children", allow_duplicate=True),
        Output(component_id='content', component_property="children", allow_duplicate=True),
        Input(component_id="initializing-btn", component_property="n_clicks"),
        [State(component_id="username", component_property="value"),
         State(component_id="password", component_property="value"),
         State(component_id="host", component_property="value"),
         State(component_id="port", component_property="value"),
         State(component_id="publishers_num", component_property="value"),
         State(component_id="publishers_topic_levels_num", component_property="value"),
         State(component_id="topic_level", component_property="value"),
         State(component_id="subscribers_num", component_property="value"),
         State(component_id="subscribers_topic_levels_num", component_property="value"),
         State(component_id="message_delay_interval", component_property="value"),
         State(component_id="payload-initial", component_property="value")
         ],
        prevent_initial_call=True
    )
    def process_initial_data(n_clicks, username, password, host, port,
                             publishers_num, publishers_topic_levels_num,
                             topic_level, subscribers_num, subscribers_topic_levels_num,
                             message_delay_interval, payload_initial):
        if n_clicks is None:
            return dash.no_update, dash.no_update
        if n_clicks:
            if None in [username, password, host, port, publishers_num, publishers_topic_levels_num,
                        subscribers_num, subscribers_topic_levels_num, topic_level,
                        message_delay_interval, payload_initial]:
                initial_form_required_fields = True
                return html.Div(className='main', id='content'), generate_initial_form_data(initial_form_required_fields, app, data, URL)
            else:
                data["username"] = username.strip()
                data["password"] = password.strip()
                data["host"] = host.strip()
                data["port"] = port
                data["publishers_num"] = publishers_num
                data["subscribers_num"] = subscribers_num
                data["publishers_topic_levels_num"] = publishers_topic_levels_num
                data["subscribers_topic_levels_num"] = subscribers_topic_levels_num
                data["topic_level"] = topic_level
                data["message_delay_interval"] = message_delay_interval
                data["payload"] = payload_initial

                response = requests.post(URL, data=data)
                response_data = json.loads(response.text)
                print(f"\nResponse: {response_data}\n")
                time.sleep(3)
                if response_data["status"] != "success":
                    if not response_data['data']['connected']:
                        return html.Div(className='main', id='content'), html.Div(
                            children=[html.H2("Unable to connect, check your password and username",
                                              style={"textAlign": "center"})])
                    return html.Div(className='main', id='content'), html.Div(
                        children=[html.H2(f"{response_data['data']}")])

                return html.Div(className='main', id='content'), generate_dashboard_components(data, app, URL, response_data["data"]["dashboard_statistics"])

    return initial_div_form_data
