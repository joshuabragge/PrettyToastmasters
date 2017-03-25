import plotly.plotly as py
import plotly
from plotly.graph_objs import *
import plotly.graph_objs as go
import private

plotly.tools.set_credentials_file(username=private.plotly_user, api_key=private.plotly_api)

def publish_graph_update(df, which_book, advanced=False):
    # Update Graph

    CC = df[df['Book'] == which_book]
    menu = []
    buttons_ = []
    all_count = []

    loops = df.shape[1] - 2
    for i in range(loops):

        # grab the names of each person we are publishing a graph for
        if advanced:
            y_ = CC.ix[:, i+2]
        else:
            y_ = CC.ix[:, i+2].apply(lambda x: 0 if x == '' else 100)
        all_count.append(list(y_))
        x_ = CC['Project']
        trace_i = go.Bar(
                        x = x_,
                        y = y_,
                        name = df.columns[i+2],
                        visible=False)
        menu.append(trace_i)

        # create the buttons which hide the other people

        false = [False for z in range(loops+1)]
        false[i] = True
        vizability = false

        button = dict(
                        args=['visible',
                        vizability],
                        label=df.columns[i+2],
                        method='restyle')
        buttons_.append(button)

    # all statistics
    all_count = [(sum(x)/loops) for x in zip(*all_count)]

    trace_all = go.Bar(
                        x = x_,
                        y = all_count,
                        name = 'all',
                        visible=True)
    menu.append(trace_all)

    # create the all_button
    false = [False for z in range(loops+1)]
    false[loops] = True
    vizability = false

    button_all = dict(
                    args=['visible',
                    vizability],
                    label='All',
                    method='restyle')

    buttons_.append(button_all)

    data = Data(menu)
    layout = Layout(
        title=which_book,
        updatemenus=list([
            dict(
                x=-0.05,
                y=1,
                yanchor='top',
                buttons=list(buttons_
                ),
            )
        ]),
    )
    fig = Figure(data=data, layout=layout)
    url = py.plot(fig, filename=which_book)
    print('Updating', which_book, 'at', url)
    return url
