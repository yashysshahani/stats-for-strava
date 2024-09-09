from strava_api import get_access_token
import requests

client_id = '130208'
client_secret = '27e2ad6b4be13544e7e02fbe523c7d20d8a52f4a'
redirect_uri = 'http://localhost:8000/exchange_token'

auth_url = f'https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope=read_all,activity:read_all'
print(f'Go to this URL and authorize the app: {auth_url}')
auth_code = input('Enter the authorization code: ')
grant_type = auth_code

token_response = get_access_token(client_id, client_secret, auth_code)
access_token = token_response['access_token']
print(f'Access Token: {access_token}')
