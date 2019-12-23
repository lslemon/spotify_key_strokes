# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:44:20 2019

@author: lukes
"""
#! /usr/bin/python
import spotipy
import requests
import urllib
import webbrowser
import json
import selenium
import time
import os
import sys

from selenium import webdriver
from spotipy import util


def authentication_request():
    client_id =  "a1e1d231ee27476faee58e646ad9dc07"
    client_secret = "f940a6bf059d4da6a37693217568a669" 
    scope ="user-modify-playback-state"
    grant_type = 'authorization_code'
    redirect_uri =  "http://localhost/"
    
    URL_AUTHENTICATION = "https://accounts.spotify.com/authorize"
    URL_TOKEN = 'https://accounts.spotify.com/api/token'
    API_URL = 'https://api.spotify.com/v1/me/player/next'
    
    params_authentication = {'client_id':client_id,
                             'response_type':'code',
                             'redirect_uri': redirect_uri,
                             'scope': scope,
                             'state':'34fFs29kd09'}
    
    urlparams = urllib.parse.urlencode(params_authentication)
    
    
    browser = webdriver.Firefox()
    browser.get(URL_AUTHENTICATION+"?"+urlparams)
    count = 0
    while redirect_uri not in browser.current_url:
        if count == 0:
            print("Waiting for response")
            count = count +1
        
    auth_response = browser.current_url
    response_params = auth_response.split('?')[1].split('&')
    code = response_params[0].replace('code=','')
    browser.close()
    return code

def token_request(code):
    
    URL_TOKEN = 'https://accounts.spotify.com/api/token'
    
    client_id =  "a1e1d231ee27476faee58e646ad9dc07"
    client_secret = "f940a6bf059d4da6a37693217568a669" 
    scope ="user-modify-playback-state"
    grant_type = 'authorization_code'
    redirect_uri =  "http://localhost/"
    
    params_token = {'client_id':client_id,
                    'client_secret':client_secret,
                    'grant_type':grant_type,
                    'code':code,
                    'scope':scope,
                    'redirect_uri':redirect_uri}
    
    urlparams = urllib.parse.urlencode(params_token)
    token_response = requests.post(URL_TOKEN, 
                                   data=params_token,
                                   verify=True)
    
    token_response_data = token_response.json()
    
    cache_file = open('.play_back_token_cache','w')
    cache_file.write(json.dumps(token_response_data))
    cache_file.close()
    
    return token_response_data
    
def next_song():
    token = access_token
    API_URL = 'https://api.spotify.com/v1/me/player/next'
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    return requests.post(API_URL, headers=headers)
    
def previous_song():
    token = access_token
    API_URL = 'https://api.spotify.com/v1/me/player/previous'
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    return requests.post(API_URL, headers=headers)    
    
def pause_song():
    token = access_token
    API_URL = 'https://api.spotify.com/v1/me/player/pause'
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    return requests.put(API_URL, headers=headers)
    
def resume_song():
    token = access_token
    API_URL = 'https://api.spotify.com/v1/me/player/play'
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    return requests.put(API_URL, headers=headers)

token_info = None
try:    
    f = open('.play_back_token_cache','w')
    token_info_string = f.read()
    f.close()
    token_info = json.loads(token_info_string)
except IOError:
    print("FUCK")

if not token_info:
    code = authentication_request()
    token_info = token_request(code)

access_token = token_info['access_token']



