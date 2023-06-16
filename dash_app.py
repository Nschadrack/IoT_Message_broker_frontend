import dash
from dash import Dash, dcc, html, Input, Output, State, dash_table
from flask import json
import requests

# import components from pages
from pages.initial_form_data import generate_initial_form_data
from pages.dashboard_components import generate_dashboard_components

app = Dash(__name__, suppress_callback_exceptions=True)
global initial_form_required_fields
global data

initial_form_required_fields = False

data = {
    "username": None,
    "password": None,
    "host": None,
    "port": None,
    "publishers_num": None,
    "subscribers_num": None,
    "publishers_topic_levels_num": None,
    "subscribers_topic_levels_num": None,
    "topic_level": None,
    "message_delay_interval": None,
    "payload": None
}
URL = "http://127.0.0.1:5599/"

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Img(src="static/images/amalitech-log.png", className="img-logo header-item"),
            html.H1("IoT Test Bench Message Broker", className="header-title header-item")]),
    ], className="header"),
    dcc.Loading(id="loading-component",
                type="circle",
                children=[html.Div(children=[
                    # Initial data form
                    generate_initial_form_data(initial_form_required_fields, app, data, URL)
                    # dashboard after submission
                ], className='main', id='content')])
])


@app.callback(
    Output(component_id='loading-component', component_property="children", allow_duplicate=True),
    Output(component_id="content", component_property="children", allow_duplicate=True),
    Input(component_id="broker_eye", component_property="n_clicks"),
    [State(component_id="publishers_num", component_property="value"),
     State(component_id="message_delay_interval", component_property="value"),
     State(component_id="publishers_topic_levels_num", component_property="value"),
     State(component_id="payload", component_property="value"),
     State(component_id="subscribers_num", component_property="value"),
     State(component_id="subscribers_topic_levels_num", component_property="value")],
    prevent_initial_call=True
)
def processing_data(n_clicks, publishers_num, message_delay_interval,
                    publishers_topic_levels_num, payload, subscribers_num,
                    subscribers_topic_levels_num):
    if n_clicks is None:
        return dash.no_update, dash.no_update
    if n_clicks:
        data["publishers_num"] = publishers_num
        data["message_delay_interval"] = message_delay_interval
        data["subscribers_topic_levels_num"] = subscribers_topic_levels_num
        data["publishers_topic_levels_num"] = publishers_topic_levels_num
        data["payload"] = payload if payload.strip() else None
        data["subscribers_num"] = subscribers_num

        if None in list(data.values()):
            initial_form_required_fields = True
            return html.Div(className='main', id='content'), generate_initial_form_data(initial_form_required_fields,
                                                                                        app, data, URL)

        response = requests.post(URL, data=data)
        response_data = json.loads(response.text)
        if response_data["status"] != "success":
            if not response_data['data']['connected']:
                return html.Div(className='main', id='content'), html.Div(
                    children=[html.H2("Unable to connect, check your password and username",
                                      style={"textAlign": "center"})])
            return html.Div(className='main', id='content'), html.Div(children=[html.H2(f"{response_data['data']}")])

        return html.Div(className='main', id='content'), generate_dashboard_components(data, app, URL, response_data["data"]["dashboard_statistics"])


if __name__ == "__main__":
    app.run_server(debug=True, port=5598)
