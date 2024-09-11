import streamlit as st
import strava_api
from activities import Activities
import data_analysis
import authorization
from urllib.parse import urlparse, parse_qs

# Title
st.title("🚴 Stats for Strava")

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
        st.link_button("Authorize with Strava", url=auth_url)

    else:
        token_response = strava_api.get_access_token(
            auth.CLIENT_ID, auth.CLIENT_SECRET, code
        )
        access_token = token_response.get("access_token")
        data = strava_api.get_athlete_data(access_token)
        all_activities = strava_api.fetch_all_activities(access_token)
        activities = Activities(all_activities)
        activities_df = activities.data
        rides_df = activities.mod_activities(sport_type="Ride", units="miles")
        cal_df = data_analysis.calendarify(rides_df)
        st.write(cal_df)
        data_analysis.cum_dist_plot(cal_df)
        data_analysis.dist_heatmap(cal_df)

    if st.session_state.get("strava_auth"):
        access_token = st.session_state["strava_auth"].get("access_token")
        if access_token:
            all_activities = authorization.fetch_all_activities(access_token)
            # Display or process the activities using Streamlit components
            st.write(all_activities)  # Example display

