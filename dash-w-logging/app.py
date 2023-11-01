from dotenv import load_dotenv
load_dotenv()
import dash
import flask
import random
import os
import json

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime
from loguru import logger

logger.info(f"logger.info(): Hello world, the app is loaded'")

# use a random number to identify a user's unique session
session_id = (random.randrange(1,100000))

logger.info(f"logger.info(): Beginning data download'")
start = datetime.now()
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
end = datetime.now()
logger.info(f"logger.info(): Data download complete. Took '{end-start}'")

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
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



@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    # identify user for logging
    user_metadata = get_credentials(flask.request)
    username = user_metadata.get("user")

    # identify pid
    pid = os.getpid()

    # You should not use `print` for logging. `print` statements will not show up 
    # in the logs immediatly.
    print(f"print(): The plot is being updated with '{value}' for user '{username}' on pid '{pid}' with session id '{session_id}'")

    # You should use a tool purpose built for logging, like the built in logging
    # library, or my preferred option `loguru`.
    logger.info(f"logger.info(): The plot is being updated with '{value}' for user '{username}' on pid '{pid}' with session id '{session_id}'")
    
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')


if __name__ == '__main__':
    app.run_server(debug=True)