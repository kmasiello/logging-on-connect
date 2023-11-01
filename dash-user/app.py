# from https://docs.posit.co/connect/user/dash/#user-meta-data
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="salutation",
    options=[
            {"label": "Hello", "value": "Hello"},
            {"label": "Greetings", "value": "Greetings"},
            {"label": "Aloha", "value": "Aloha"},
    ],
        searchable=False,
        clearable=False,
        value="Hello"
    ),
    html.P(id="greeting")
])


def get_credentials(req):
    """
    Returns a dict containing "user" and "groups" information populated by
    the incoming request header "RStudio-Connect-Credentials".
    """
    credential_header = req.headers.get("RStudio-Connect-Credentials")
    if not credential_header:
        return {}
    return json.loads(credential_header)


@app.callback(
    Output(component_id="greeting", component_property="children"),
    [Input("salutation", "value")]
)
def greeting(salutation):
    user_metadata = get_credentials(flask.request)
    username = user_metadata.get("user")
    return "%s, %s." % (salutation, username or "stranger")

if __name__ == "__main__":
    app.run_server(debug=True)
