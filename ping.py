from datetime import datetime
from pythonping import ping

import dash
from dash import Input, Output, dcc, html
import plotly.graph_objects as go

list_v, list_t = [], []

app = dash.Dash(__name__, update_title="ping")
app.layout = html.Div([
    html.H1('Live update ping chart'),
    dcc.Graph(id='graph', figure={}), 
    dcc.Interval(id="interval", interval=1*1000, n_intervals=0)
])


@app.callback(Output('graph', 'figure'), Input('interval', 'n_intervals'))
def update_data(n_intervals):
    global list_v, list_t # :P
    
    samples = 180
    hi_lim = 100.0
    ip = '8.8.8.8'
    ip_timeout = 0.5
    
    list_t.append(datetime.now())
    list_v.append(myping(ip, ip_timeout))
    list_t = list_t[-samples:]
    list_v = list_v[-samples:]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list_t, y=list_v))
    fig.update_layout(
        hovermode="x unified",
        title=f"<b>> ping {ip}</b><br><a target='_blank' href='https://www.linkedin.com/in/CesarBecerraCO'><span style='font-size:12px;'>linkedin.com/in/CesarBecerraCO</span></a>",
        yaxis_title="ms",
        xaxis_title="timestamp",
        yaxis_range=[0,None],
        yaxis={'side': 'right'} 
    )
    fig.add_hline(y=hi_lim, line={'dash': 'dash', 'color': 'red'})

    return fig


def myping(ip, timeout):
    res = str(ping(ip, size=40, count=1, verbose=False, timeout=timeout).__dict__['_responses'][0]).split()[-1]
    return None if res == "out" else float(res.replace("ms", ""))

if __name__ == '__main__':
    app.run_server()
