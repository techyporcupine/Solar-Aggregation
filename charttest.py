import plotly.graph_objects as go

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 56.33,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Kilowatts", 'font': {'size': 56}},
    gauge = {'axis': {'range': [None, 100]}}))

fig.show()
