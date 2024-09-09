from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

def calc_cum_dist(df):
    df["distance"] = df["distance"].fillna(0)

    years = range(df["year"].min(), datetime.now().year + 1)
    df.loc[:, "yearly_cum_dist"] = 0.0

    for year in years:
        sub_df = df[df["year"] == year].copy()
        sub_df["yearly_cum_dist"] = sub_df["distance"].cumsum().astype(float)
        df.loc[df["year"] == year, "yearly_cum_dist"] = sub_df["yearly_cum_dist"]

    return df

def calendarify(data):
    data["start_date"] = pd.to_datetime(data["start_date"], errors='coerce')
    data["year"] = data["start_date"].dt.year
    data["mthday"] = pd.to_datetime(data["start_date"].dt.strftime("%d-%b"), format='%d-%b', errors='coerce')
    data["yearmthday"] = pd.to_datetime(data["start_date"].dt.strftime("%Y-%d-%b"), format='%Y-%d-%b', errors='coerce')
    data = data.sort_values("start_date").reset_index(drop=True)

    start_year = data["year"].min()
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    all_dates = pd.date_range(start=start_date, end=end_date, name="yearmthday").to_frame(index=False)
    all_dates["year"] = all_dates["yearmthday"].dt.year
    all_dates["mthday"] = all_dates["yearmthday"].dt.strftime("%m-%d")
    all_dates["mthday"] = pd.to_datetime(all_dates["mthday"], format='%m-%d', errors='coerce')

    data = pd.merge(all_dates, data, on=["yearmthday", "mthday", "year"], how="left")

    data = calc_cum_dist(data)
    return data

def cum_dist_plot(data):
    fig = px.line(data, x='mthday', y='yearly_cum_dist', color='year',
              title='Yearly Cumulative Distance',
              labels={'mthday': 'Date', 'yearly_cum_dist': f'Yearly Cumulative Distance ({activities.units})'},
             line_shape="hv")
    fig.update_layout(xaxis=dict(tickformat="%b-%d"))
    fig.update_traces(connectgaps=True)
    fig.show(renderer='plotlyshare')

def activity_dist_scatter(data):
    filtered_df = data[data['distance'] != 0]
    fig = px.scatter(filtered_df, x='mthday', y='distance', size='distance', color='year',
                title='Distance Scatter',
                labels={'mthday': 'Date', 'distance': f'Distance ({activities.units})'})
    fig.update_layout(xaxis=dict(tickformat="%b-%d"))
    fig.update_traces(connectgaps=True)
    fig.show(renderer='plotlyshare')

def dist_freq_hist(data):
    filtered_df = data[data['distance'] != 0]
    fig = px.histogram(filtered_df, x='distance', color='year',
                title='Mileage Frequency',
                labels={'mthday': 'Date', 'distance': f'Distance ({activities.units})'})
    fig.update_layout(xaxis=dict(tickformat="%b-%d"))
    fig.show(renderer='plotlyshare')
