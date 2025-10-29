import pandas as pd
import plotly.graph_objects as go

# --- Load and prepare data ---
df = pd.read_csv("region_05_clean.csv", encoding='latin1')

# More efficient aggregation
attack_pivot = (
    df.groupby(['iyear', 'attacktype1_txt'])
    .size()
    .unstack(fill_value=0)
)

# --- Create Figure ---
fig = go.Figure()

# Pre-calculate number of traces
n_traces = len(attack_pivot.columns)

# Add traces
fig.add_traces([
    go.Scatter(
        x=attack_pivot.index,
        y=attack_pivot[attack_type],
        mode='lines',
        stackgroup='one',
        name=attack_type,
        hovertemplate=(
            '<b>Year:</b> %{x}<br>'
            f'<b>Attack Type:</b> {attack_type}<br>'
            '<b>Incidents:</b> %{y}<extra></extra>'
        )
    )
    for attack_type in attack_pivot.columns
])

# --- Update layout with working buttons ---
fig.update_layout(
    title={
        'text': "Attack Types Over Time - Region 05",
        'x': 0.98,
        'y': 0.98,
        'xanchor': 'right',
        'yanchor': 'top'
    },
    xaxis_title="Year",
    yaxis_title="Number of Incidents",
    hovermode="x unified",
    template="plotly_white",
    legend_title="Attack Types",
    updatemenus=[{
        'type': "buttons",
        'direction': "right",
        'x': 0.5,
        'y': 1.15,
        'xanchor': 'center',
        'showactive': True,
        'buttons': [
            {
                'label': "Stacked",
                'method': "update",
                'args': [
                    {
                        'stackgroup': ['one'] * n_traces,
                        'groupnorm': [''] * n_traces
                    },
                    {
                        'yaxis.title.text': 'Number of Incidents'
                    }
                ]
            },
            {
                'label': "Grouped",
                'method': "update",
                'args': [
                    {
                        'stackgroup': [''] * n_traces,
                        'groupnorm': [''] * n_traces
                    },
                    {
                        'yaxis.title.text': 'Number of Incidents'
                    }
                ]
            },
            {
                'label': "100% Stacked",
                'method': "update",
                'args': [
                    {
                        'stackgroup': ['one'] * n_traces,
                        'groupnorm': ['percent'] * n_traces
                    },
                    {
                        'yaxis.title.text': 'Percentage of Incidents'
                    }
                ]
            }
        ]
    }]
)

# fig.show()

# specify a port explicitly:
import plotly.offline as pyo
pyo.plot(fig, filename='attack_types.html', auto_open=True)

# create a seperate html file to run 
# fig.write_html("attack_types_visualization.html")
# print("Visualization saved! Open 'attack_types_visualization.html' in your browser")