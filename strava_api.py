import requests

def get_access_token(client_id, client_secret, code):
    response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )
    return response.json()

def get_athlete_data(access_token):
    response = requests.get(
        'https://www.strava.com/api/v3/athlete',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return response.json()

def get_activities(access_token, per_page=30, page=1):
    response = requests.get(
        f'https://www.strava.com/api/v3/athlete/activities?per_page={per_page}&page={page}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return response.json()

def fetch_all_activities(access_token):
    activities = []
    page = 1
    per_page = 30

    while True:
        response = requests.get(
            'https://www.strava.com/api/v3/athlete/activities',
            headers={'Authorization': f'Bearer {access_token}'},
            params={'per_page': per_page, 'page': page}
        )

        if response.status_code == 200:
            current_activities = response.json()
            activities.extend(current_activities)
            page += 1 # move to next page
    
            # check if we at end of ativities
            if len(current_activities) < per_page:
                break
        else:
            print(f"Failed to fetch activities. Status code: {response.status_code}")
            break
    return activities
