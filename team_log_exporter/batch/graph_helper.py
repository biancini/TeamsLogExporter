from requests_oauthlib import OAuth2Session
import requests

graph_url = 'https://graph.microsoft.com/v1.0'

def _get_request_heads(token):
    return {
        'authorization': 'Bearer {0}'.format(token),
        'authority': 'api.interfaces.records.teams.microsoft.com',
        'scheme': 'https',
        'accept': 'application/json',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'x-request-id': '0a4d2ce9-db69-4c2a-9ab1-44fe31f7b6a1',
        'origin': 'https://admin.teams.microsoft.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mod': 'cors',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'
    }

def _remove_duplicates(lista, key='id'):
    ritorno = []
    keys = []

    for item in lista:
        if item[key] not in keys:
            keys.append(item[key])
            ritorno.append(item)

    return ritorno

def get_meuser(token):
    graph_client = OAuth2Session(token=token)
    user = graph_client.get('{0}/me'.format(graph_url)).json()
    return user

def get_otheruser(token, uid):
    graph_client = OAuth2Session(token=token)
    user = graph_client.get('{0}/users/{1}'.format(graph_url, uid)).json()
    return user

def get_all_groups(token):
    graph_client = OAuth2Session(token=token)

    lista = []
    uri = '{0}/groups'.format(graph_url)
    
    while uri is not None:
        result = graph_client.get(uri).json()
        if not 'value' in result:
            raise Exception(result['error']['message'] if 'error' in result else 'Unknown error')
        lista.extend(result['value'])

        uri = result['@odata.nextLink'] if '@odata.nextLink' in result else None

    return lista

def get_all_users(token):
    graph_client = OAuth2Session(token=token)
    
    lista = []
    uri = '{0}/users'.format(graph_url)

    while uri is not None:
        result = graph_client.get(uri).json()
        if not 'value' in result:
            raise Exception(result['error']['message'] if 'error' in result else 'Unknown error')
        lista.extend(result['value'])
        uri = result['@odata.nextLink'] if '@odata.nextLink' in result else None

    return _remove_duplicates(lista, 'id')

def get_group_users(token, groupid):
    graph_client = OAuth2Session(token=token)
    
    lista = []
    uri = '{0}/groups/{1}/owners'.format(graph_url, groupid)

    while uri is not None:
        result = graph_client.get(uri).json()
        if not 'value' in result:
            raise Exception(result['error']['message'] if 'error' in result else 'Unknown error')
        lista.extend(result['value'])
        uri = result['@odata.nextLink'] if '@odata.nextLink' in result else None

    uri = '{0}/groups/{1}/members'.format(graph_url, groupid)

    while uri is not None:
        result = graph_client.get(uri).json()
        if not 'value' in result:
            raise Exception(result['error']['message'] if 'error' in result else 'Unknown error')
        lista.extend(result['value'])
        uri = result['@odata.nextLink'] if '@odata.nextLink' in result else None

    return _remove_duplicates(lista, 'id')

def get_user_meetings(token, userid):
    headers = _get_request_heads(token)
    headers['path'] = '/Skype.Analytics/Users(\'{0}\')/Communications?%24top=500'.format(userid)
    headers['referer'] = 'https://admin.teams.microsoft.com/users/{0}/activity'.format(userid)

    lista = []
    uri = 'https://api.interfaces.records.teams.microsoft.com/Skype.Analytics/Users(\'{0}\')/Communications?%24top=500'.format(userid)

    while uri is not None:
        result = requests.get(uri, headers=headers).json()
        if not 'value' in result:
            raise Exception(result['message'] if 'message' in result else 'Unknown error')
        lista.extend(result['value'])
        
        uri = result['@odata.nextLink'] if '@odata.nextLink' in result else None

    return _remove_duplicates(lista, 'id')

def get_meeting_records(token, userid, meetingid):
    headers = _get_request_heads(token)
    headers['path'] = '/Skype.Analytics/Communications(\'{0}\')/Participants'.format(meetingid)
    headers['referer'] = 'https://admin.teams.microsoft.com/users/{0}/meeting/{1}'.format(userid, meetingid)

    lista = []
    uri = 'https://api.interfaces.records.teams.microsoft.com/Skype.Analytics/Communications(\'{0}\')/Participants'.format(meetingid)
    
    while uri is not None:
        result = requests.get(uri, headers=headers).json()
        if not 'value' in result:
            raise Exception(result['message'] if 'message' in result else 'Unknown error')
        lista.extend(result['value'])
        uri = result['@odata.nextLink'] if '@odata.nextLink' in result else None
    
    return lista
