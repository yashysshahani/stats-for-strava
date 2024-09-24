import streamlit as st
import pandas as pd

def cum_metric(data):
    units = data.units
    data = data.data

    current_year_df = data[data["year"] == data["year"].max()]
    latest_dist = current_year_df["yearly_cum_dist"].max()
    current_month = current_year_df[current_year_df["yearly_cum_dist"] == latest_dist]["month"].values[0]
    current_day = current_year_df[current_year_df["yearly_cum_dist"] == latest_dist]["day_of_month"].values[0]
    last_year = int(data["year"].max()) - 1
    last_year_df = data[data["year"] == str(last_year)]
    try:
        dist_last_year = last_year_df[(last_year_df["month"] == current_month) & (last_year_df["day_of_month"] == current_day)]["yearly_cum_dist"].values[0]
    except IndexError:
        try:
            dist_last_year = last_year_df[(last_year_df["month"] == current_month) & (last_year_df["day_of_month"] == current_day - 1)]["yearly_cum_dist"].values[0]
        except IndexError:
            return

    # clean up metrics
    latest_dist = round(latest_dist, 2)
    dist_last_year = round(dist_last_year, 2)
    delta = round(latest_dist - dist_last_year, 2)
    if dist_last_year == 0:
        delta_percentage = 100
    else:
        delta_percentage = round((delta / dist_last_year) * 100, 2)

    metric = st.metric(f"Distance in {data['year'].max()}:", value=f"{latest_dist} {units}",
                delta=f"{delta} ({delta_percentage}%) from today, {last_year}!", delta_color="normal")
    return metric

def cum_activity_metric(data):
    data = data.data
    current_year_df = data[data["year"] == data["year"].max()]
    latest_activities = current_year_df["yearly_cum_activities"].max()
    current_month = current_year_df[current_year_df["yearly_cum_activities"] == latest_activities]["month"].values[0]
    current_day = current_year_df[current_year_df["yearly_cum_activities"] == latest_activities]["day_of_month"].values[0]
    last_year = int(data["year"].max()) - 1
    last_year_df = data[data["year"] == str(last_year)]
    try:
        activities_last_year = last_year_df[(last_year_df["month"] == current_month) & (last_year_df["day_of_month"] == current_day)]["yearly_cum_activities"].values[0]
    except IndexError:
        try:
            activities_last_year = last_year_df[(last_year_df["month"] == current_month) & (last_year_df["day_of_month"] == current_day - 1)]["yearly_cum_activities"].values[0]
        except IndexError:
            return

    delta = latest_activities - activities_last_year
    delta_percentage = round((delta / activities_last_year) * 100, 2)

    metric = st.metric(f"Activities in {data['year'].max()}:", value=f"{latest_activities}",
                delta=f"{delta} ({delta_percentage}%) from today, {last_year}!", delta_color="normal")
    return metric
