from datetime import datetime
import pandas as pd
from activities import Activities
import streamlit as st

def calc_cum_dist(df):
    df["distance"] = df["distance"].fillna(0)

    years = range(df["year"].min(), datetime.now().year + 1)
    df.loc[:, "yearly_cum_dist"] = 0.0

    for year in years:
        sub_df = df[df["year"] == year].copy()
        sub_df["yearly_cum_dist"] = sub_df["distance"].cumsum().astype(float)
        df.loc[df["year"] == year, "yearly_cum_dist"] = sub_df["yearly_cum_dist"]

    return df

def calendarify(data, units):
    st.cache_data.clear()
    # Convert start_date to datetime and extract year, month, and formatted dates
    data["start_date"] = pd.to_datetime(data["start_date"], errors='coerce')
    data["year"] = data["start_date"].dt.year
    data["month"] = data["start_date"].dt.month
    data["mthday"] = data["start_date"].dt.strftime("%d-%b")
    data["yearmthday"] = data["start_date"].dt.strftime("%Y-%d-%b")

    # Generate a complete date range from the start year to now
    start_year = data["year"].min()
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    all_dates = pd.date_range(start=start_date, end=end_date, name="yearmthday").to_frame(index=False)
    all_dates["year"] = all_dates["yearmthday"].dt.year
    all_dates["month"] = all_dates["yearmthday"].dt.month
    all_dates["mthday"] = all_dates["yearmthday"].dt.strftime("%d-%b")
    all_dates["yearmthday"] = all_dates["yearmthday"].dt.strftime("%Y-%d-%b")

    # Merge the complete date range with the original data
    data = pd.merge(all_dates, data, on=["yearmthday", "mthday", "year", "month"], how="left")
    data["name"] = data["name"].fillna("-")

    # Calculate cumulative distance
    data = calc_cum_dist(data)

    return Activities(data, units=units)
