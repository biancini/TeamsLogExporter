import os
import sys
import requests
import pyodbc
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


def get_client_credentials(ente):
    tenant_id = os.getenv(f'TENANTID_{ente}', None)
    client_id = os.getenv(f'APPID_{ente}', None)
    client_secret =  os.getenv(f'APPSECRET_{ente}', None)

    return {
        'tenant_id': tenant_id,
        'client_id': client_id,
        'client_secret': client_secret
    }


def connect_perseo_db():
    server = os.getenv('PERSEO_IP', None)
    database = os.getenv('PERSEO_DB', None)
    username = os.getenv('PERSEO_USR', None)
    password = os.getenv('PERSEO_PWD', None)

    conn_string = 'DRIVER={FreeTDS};SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password+';Trusted_Connection=no'
    conn = pyodbc.connect(conn_string)
    
    return conn