from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import pandas as pd
from activities import Activities

def calc_cum_dist(df):
    df["distance"] = df["distance"].fillna(0)

    years = range(df["year"].min(), datetime.now().year + 1)
    df.loc[:, "yearly_cum_dist"] = 0.0

    for year in years:
        sub_df = df[df["year"] == year].copy()
        sub_df["yearly_cum_dist"] = sub_df["distance"].cumsum().astype(float)
        df.loc[df["year"] == year, "yearly_cum_dist"] = sub_df["yearly_cum_dist"]

    return df

from datetime import datetime
import pandas as pd

def calendarify(data):
    df = data.data
    # Convert start_date to datetime and extract year, month, and formatted dates
    df["start_date"] = pd.to_datetime(df["start_date"], errors='coerce')
    df["year"] = df["start_date"].dt.year
    df["month"] = df["start_date"].dt.month
    df["mthday"] = df["start_date"].dt.strftime("%d-%b")
    df["yearmthday"] = df["start_date"].dt.strftime("%Y-%d-%b")

    # Sort data by start_date
    df = df.sort_values("start_date").reset_index(drop=True)

    # Generate a complete date range from the start year to now
    start_year = df["year"].min()
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    all_dates = pd.date_range(start=start_date, end=end_date, name="yearmthday").to_frame(index=False)
    all_dates["year"] = all_dates["yearmthday"].dt.year
    all_dates["month"] = all_dates["yearmthday"].dt.month
    all_dates["mthday"] = all_dates["yearmthday"].dt.strftime("%d-%b")
    all_dates["yearmthday"] = all_dates["yearmthday"].dt.strftime("%Y-%d-%b")  # Ensure same format as data

    # Merge the complete date range with the original data
    df = pd.merge(all_dates, df, on=["yearmthday", "mthday", "year", "month"], how="left")

    # Calculate cumulative distance
    df = calc_cum_dist(df)
    return Activities(data, units=data.units)

def cum_dist_plot(data):
    df = data.data
    fig = px.line(df, x='mthday', y='yearly_cum_dist', color='year',
              title='Yearly Cumulative Distance',
              labels={'mthday': 'Date', 'yearly_cum_dist': f'Yearly Cumulative Distance ({data.units})'},
             line_shape="hv")
    fig.update_layout(xaxis=dict(tickformat="%b-%d"))
    fig.update_traces(connectgaps=False)
    st.plotly_chart(fig)
    
    return fig

def activity_dist_scatter(data):
    df = data.data
    filtered_df = df[df['distance'] != 0]
    fig = px.scatter(filtered_df, x='mthday', y='distance', size='distance', color='year',
                title='Distance Scatter',
                labels={'mthday': 'Date', 'distance': f'Distance ({data.units})'})
    fig.update_layout(xaxis=dict(tickformat="%b-%d"))
    fig.update_traces(connectgaps=True)

    fig = st.plotly_chart(fig)
    return fig

def dist_freq_hist(data):
    df = data.data
    filtered_df = df[df['distance'] != 0]
    fig = px.histogram(filtered_df, x='distance', color='year',
                title='Mileage Frequency',
                labels={'mthday': 'Date', 'distance': f'Distance ({data.units})'})
    fig.update_layout(xaxis=dict(tickformat="%b-%d"))
    
    fig = st.plotly_chart(fig)
    return fig

def dist_heatmap(data):
    df = data.data
    fig = px.density_heatmap(df,
                             x = "year",
                             y = "month",
                             z = "distance",
                             title = "Distance Heatmap")
    fig = st.plotly_chart(fig)

    return fig
