# import requests
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
    'Authorization': 'Basic ' + auth_base64,
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)


    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_auth_header(token):
    return{'Authorization':'Bearer '+ token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1' #spotify api already takes care of spaces and lowercase etc

    query_url = url + query
    result = get(query_url, headers=headers)

    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print('this artist does not exist')
        return None

    return json_result[0]

    
token = get_token()
result = search_for_artist(token, "olivia rodrigo") 
artist_id = result['id']
print(artist_id)

artist_1_name = input('Enter the first artist: ')
artist_2_name  = input('Enter the second artist: ')

token = get_token()
result_1 = search_for_artist(token, artist_1_name) 
artist_1_id = result_1['id']

result_2 = search_for_artist(token, artist_2_name) 
artist_2_id = result_2['id']

print(f'id of first artist: {artist_1_id}')
print(f'id of second artist: {artist_2_id}')


#Give user option to view playlist first and shuffle to a new one, before creating it for them on spotify