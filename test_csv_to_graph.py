# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:28:37 2020

@author: Contra
"""
from starlette.requests import Request
from starlette.responses import Response
import pandas as pd
import json
import plotly.graph_objs as go
import plotly
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.applications import Starlette
from sklearn import preprocessing

templates = Jinja2Templates(directory='templates')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}



def create_plot_normalize():


    csv_name=('fooo.csv')
    df = pd.read_csv(csv_name)
    scaler = preprocessing.MinMaxScaler()

    names =df.columns
    d = scaler.fit_transform(df)

    scaled_df = pd.DataFrame(d, columns=names)
    data = [
        go.Bar(
            x=scaled_df[df.columns[0]], # assign x as the dataframe column 'x'
            y=scaled_df[df.columns[1]]
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_plot():


    csv_name=('fooo.csv')
    df = pd.read_csv(csv_name)
    
    data = [
        go.Bar(
            x=df[df.columns[0]], # assign x as the dataframe column 'x'
            y=df[df.columns[1]]
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    fp = open('fooo.csv', 'wb')
    body = b''
    async for chunk in request.stream():
        body += chunk
        
    response = Response(body, media_type='SpooledTemporaryFile')
    fp.write(body)
    await response(scope, receive, send)

async def homepage(request):
    bar = create_plot()
    plot2 = create_plot_normalize()
    return templates.TemplateResponse('index.html',{"request": request, 'plot' :bar, 'plot2':plot2})

routes = [
    Route('/graph', endpoint=homepage),
    Mount('/', app)
]

app = Starlette(debug=False, routes=routes)