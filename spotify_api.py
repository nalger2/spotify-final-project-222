# Used and modified Gina Sprint's code from https://github.com/GonzagaCPSC222/U7-APIs-NLP/blob/master/APIFun/Spotify.ipynb

import requests
import json 
import base64
import numpy as np 
import pandas as pd

client_ID = "9c36bcb992fa4c459a7c80cc941f9605"
client_secret = "5818be1605f74f4eb4caf2b10f1e318b"

auth_endpoint = "https://accounts.spotify.com/api/token"
search_API_endpoint = "https://api.spotify.com/v1/search"

# get access token to use for authentication with search api
def get_access_token():
    # from Spotify docs:
    # Required: Base 64 encoded string that contains the client ID and client secret key. 
    # The field must have the format: 
    # Authorization: Basic *<base64 encoded client_id:client_secret>*
    message = client_ID + ":" + client_secret
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    encoded_client_details = base64_bytes.decode("ascii")
    
    headers = {"Authorization": "Basic " + encoded_client_details}              
    body = {"grant_type": "client_credentials"}
    response = requests.post(url=auth_endpoint, headers=headers, data=body)
    json_object = json.loads(response.text)
    return json_object["access_token"]
    
# make the request using requests module
# need to send the access token via request headers
def make_request(access_token, full_url):
    headers = {"Accept": "application/json", 
               "Content-Type": "application/json", 
               "Authorization": "Bearer " + access_token}

    response = requests.get(url=full_url, headers=headers)
    json_object = json.loads(response.text)
    return json_object

# loop through songs, create request url, make search request, return list of song popularities
def get_song_popularities(access_token, search_terms, search_type):
    #pop_ser = pd.Series(dtype=int)
    pop_list = []
    for item in search_terms:
        search_term = requests.utils.quote(item)
        search_type = requests.utils.quote(search_type)
        url = search_API_endpoint + "?q=" + search_term
        url += "&type=" + search_type
        json_obj = make_request(access_token, url)
        tracks = json_obj["tracks"]
        items = tracks["items"]
        if(len(items) > 0):
            first_track_item = items[0]
            popularity = first_track_item["popularity"]
            pop_list.append(popularity)
        else:
            pop_list.append(np.nan)
    return pop_list

def add_popularity_column(df):
    access_token = get_access_token()
    pop_list = get_song_popularities(access_token, df["trackName"] + " " + df["artistName"], "track")
    df["song popularity"] = pop_list
