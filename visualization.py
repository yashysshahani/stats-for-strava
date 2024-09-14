import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import pandas as pd
from activities import Activities


colors = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600', '#631A86', '#C45AB3', '#F45866', '#F49390', '#7776BC']

def generate_ref_df():
    reference_df = pd.date_range(start='2000-01-01', end='2000-12-31', freq='D').to_frame(index=False)
    reference_df["mthday"] = reference_df[0].dt.strftime("%d-%b")
    reference_df["yearmthday"] = reference_df[0].dt.strftime("%Y-%d-%b")
    reference_df["year"] = reference_df[0].dt.year
    reference_df["month"] = reference_df[0].dt.month
    reference_df["distance"] = 0
    reference_df["yearly_cum_dist"] = 0.0

    return reference_df

def cum_dist_plot(data):
    df = data.data
    fig = go.Figure()
    reference_df = generate_ref_df()
    
    # Add reference line
    fig.add_trace(go.Scatter(x=reference_df["mthday"], y=reference_df["yearly_cum_dist"],
                                mode='lines', name='Reference', line=dict(color='black', width=1),
                                showlegend=False, hoverinfo='skip', connectgaps=False, opacity=0))
    
    lines = px.line(df, x='mthday', y='yearly_cum_dist', color='year',
                       line_shape="spline", color_discrete_sequence=px.colors.sequential.Plasma,
                       hover_name='name',  hover_data={'year': True, 'mthday': False, 'yearly_cum_dist': True,
                                                       'name': False})
    
    for trace in lines.data:
        fig.add_trace(trace)
    
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
            ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            title='Month'
        ),
        yaxis=dict(title=f'Yearly Cumulative Distance ({data.units})'),
        title='Yearly Cumulative Distance',
        showlegend=True,
        legend=dict(title='Year'),
        hovermode='x',
        hoverlabel=dict(font_size=12, font_family='Arial'),
    )
    
    fig.update_traces(connectgaps=False)
    
    fig = st.plotly_chart(fig)
    
    return fig

def activity_dist_scatter(data):
    reference_df = generate_ref_df()
    df = data.data[data.data['distance'] != 0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=reference_df["mthday"], y=reference_df["distance"],
                                mode='lines', name='Reference', line=dict(color='black', width=1),
                                  showlegend=False, hoverinfo='skip', connectgaps=False, opacity=0))
    df["year"] = df["year"].astype(str)
    dots = px.scatter(df, x='mthday', y='distance', color='year',
                title='Distance Scatter', color_discrete_sequence=px.colors.sequential.Plasma)
    
    for trace in dots.data:
        fig.add_trace(trace)
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330],
            ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        ))
    fig = st.plotly_chart(fig)
    return fig

def dist_freq_hist(data):
    df = data.data
    filtered_df = df[df['distance'] != 0]
    fig = px.histogram(filtered_df, x='distance', color='year',
                title='Mileage Frequency',
                labels={'mthday': 'Date', 'distance': f'Distance ({data.units})'},
                color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(xaxis=dict(tickformat="%b"))
    
    fig = st.plotly_chart(fig)
    return fig

def dist_heatmap(data):
    df = data.data
    df["year"] = df["year"].astype(str)
    fig = px.density_heatmap(df,
                             x = "year",
                             y = "month",
                             z = "distance",
                             title = "Distance Heatmap",
                             color_continuous_scale=px.colors.sequential.Plasma)
    fig = st.plotly_chart(fig)

    return fig
