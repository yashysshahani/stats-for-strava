import streamlit as st
import strava_api
from activities import Activities
import data_analysis
import authorization
import visualization
import text

def page(): 

    access_token = st.session_state.access_token

    col1, col2 = st.columns(2)
    selected_activity = col1.selectbox("Select Activity Type", ["Ride", "Run", "Swim", 
                                                                "AlpineSki", "BackcountrySki", "Canoeing", "Crossfit",
                                                                "EBikeRide", "Elliptical", "Golf", "Handcycle", "Hike", "IceSkate",
                                                                "InlineSkate", "Kayaking", "Kitesurf", "NordicSki",
                                                                "RockClimbing", "RollerSki", "Rowing",
                                                                "Sail", "Skateboard", "Snowboard", "Snowshoe", "Soccer",
                                                                "StairStepper", "StandUpPaddling", "Surfing",
                                                                "Velomobile", "VirtualRide", "VirtualRun", "Walk",
                                                                  "WeightTraining", "Wheelchair", "Windsurf", "Workout", "Yoga"])
    selected_unit = col2.selectbox("Select Distance Unit", ["Miles", "Kilometers"])

    if st.button("Generate nerd stuff..."):

        try:
            all_activities = strava_api.fetch_all_activities(access_token)
            activities = Activities(all_activities)
            activity_df = activities.mod_activities(sport_type=selected_activity, units=selected_unit)
            cal_activities = data_analysis.calendarify(activity_df, units=selected_unit)

        except TypeError:
            st.write(f"An error occurred while processing your data for {selected_activity}.")

        text.cum_metric(cal_activities)

        tab1, tab2, tab3, tab4 = st.tabs(["Cumulative Distance", "Activity Distribution", "Distance Frequency", "Distance Heatmap"])
        with tab1:
            visualization.cum_dist_plot(cal_activities)
        with tab2: 
            visualization.activity_dist_scatter(cal_activities)
        with tab3:
            visualization.dist_freq_hist(cal_activities)
        with tab4:
            visualization.dist_heatmap(cal_activities)

