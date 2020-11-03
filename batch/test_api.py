import requests
import os.path
from urllib import parse

def call_api(t, uri):
    head = { 'Authorization': f'Bearer {t}' }
    r = requests.get(uri, headers=head)
    response = r.json()

    return response

if __name__ == '__main__':
    tenant_id = os.getenv('TENANTID_ENAIP', None)
    client_id = os.getenv('APPID_ENAIP', None)
    client_secret =  os.getenv('APPSECRET_ENAIP', None)
    
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
        
    t = r['access_token']

    #user_id = '5b8e3fb3-efed-43d2-a23e-0f668cd9c975'
    call_id =  '19:8c87ed3fe140463793daffac2c6adc8e@thread.tacv2'
    #uri = f'https://graph.microsoft.com/beta/communications/callRecords/{call_id}?$expand=sessions($expand=segments)'
    uri = f'https://graph.microsoft.com/v1.0/communications/onlineMeetings'
    response = call_api(t, uri)
    print (f'{response}')

    print(f'Script finito.')