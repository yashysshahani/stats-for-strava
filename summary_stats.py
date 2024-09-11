import strava_api
from activities import Activities
import data_analysis

def get_data(access_token, selected_activity, selected_unit):
    all_activities = strava_api.fetch_all_activities(access_token)
    activities = Activities(all_activities)
    activity_df = activities.mod_activities(sport_type=selected_activity, units=selected_unit)
    cal_activities = data_analysis.calendarify(activity_df)
    cal_df = cal_activities.data

    return cal_df
