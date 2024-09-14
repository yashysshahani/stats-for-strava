import streamlit as st
import strava_api
from activities import Activities
import data_analysis
import authorization
from urllib.parse import urlparse, parse_qs
import visualization

# Title
st.title("🚴 Stats for Strava")
st.subheader("Stats for Strava is still in its infancy! Many more features coming soon...")

def get_strava_code():
    try:
        code = st.query_params["code"]
    except KeyError:
        return False
    return code

# Authorization
if __name__ == "__main__":
    auth = authorization.Authorization()
    code = get_strava_code()

    if not code:
        st.subheader("Welcome!")
        st.write("Hit the authorization button below to get insights.")

        # Strava Authorization Button
        auth_url = auth.get_auth_url()
        st.link_button("Connect with Strava", url=auth_url)

    else:
        col1, col2 = st.columns(2)
        selected_activity = col1.selectbox("Select Activity Type", ["Ride", "Run", "Swim", "Other"])
        selected_unit = col2.selectbox("Select Distance Unit", ["Miles", "Kilometers"])

        if st.button("Show Activities"):
            token_response = strava_api.get_access_token(
            auth.CLIENT_ID, auth.CLIENT_SECRET, code
            )
            access_token = token_response.get("access_token")
            all_activities = strava_api.fetch_all_activities(access_token)
            activities = Activities(all_activities)
            if 'activities' not in st.session_state:
                st.session_state.activities = activities
            activities = st.session_state.activities
            activity_df = activities.mod_activities(sport_type=selected_activity, units=selected_unit)
            cal_activities = data_analysis.calendarify(activity_df, units=selected_unit)

            visualization.cum_dist_plot(cal_activities)
            visualization.activity_dist_scatter(cal_activities)
            visualization.dist_freq_hist(cal_activities)
            visualization.dist_heatmap(cal_activities)

