import os
import sys
import requests
from urllib import parse
from datetime import datetime, timedelta


def nearestsunday():
    d = datetime.now()
    d += timedelta(days = -1 - d.weekday()) # Last Sunday
    if d.weekday() >= 3: # If Thursday or later
        d += timedelta(days = 7) # Next Sunday
    
    return d


def allsundays(years):
    for year in years:
        d = datetime(year, 1, 1)                # January 1st
        d += timedelta(days = 6 - d.weekday())  # First Sunday
        while d.year == year:
            yield d
            d += timedelta(days = 7)


def get_access_token(ente):
    tenant_id = os.getenv(f'TENANTID_{ente}', None)
    client_id = os.getenv(f'APPID_{ente}', None)
    client_secret =  os.getenv(f'APPSECRET_{ente}', None)

    data = parse.urlencode({
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    })

    uri = 'https://login.microsoftonline.com/{0}/oauth2/v2.0/token'.format(tenant_id)
    r = requests.post(uri, data=data).json()

    if not 'access_token' in r:
        print(f'{r}')
        sys.exit(1)

    return r['access_token']


def get_user_credentials():
    username = os.getenv('USER_NAME', None)
    password = os.getenv('PASSWORD', None)

    return {
        'username': username,
        'password': password
    }