import requests
import json
import os.path
from urllib import parse

'''
Scaricare i dati dal report creato appostivamente qui:
https://cqd.teams.microsoft.com/spd/#/Dashboard?language=it-IT
'''


def get_berarertoken(ente):
    tenant_id = os.environ[f'TENANTID_{ente}']
    client_id = os.environ[f'APPID_{ente}']
    client_secret =  os.environ[f'APPSECRET_{ente}']

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
        exit(1)    
    return r['access_token']


def download_call_data(t, call_id):
    uri = f'https://graph.microsoft.com/beta/communications/callRecords/{call_id}?$expand=sessions($expand=segments)'
    head = { 'Authorization': f'Bearer {t}' }
    r = requests.get(uri, headers=head)
    response = r.json()

    if 'error' in response:
        print (f'{response}')
        return None
    else:
        return json.dumps(response, indent=4)