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
    groups = graph_client.get('{0}/groups'.format(graph_url)).json()
    return groups['value'] if 'value' in groups else []

def get_all_users(token):
    graph_client = OAuth2Session(token=token)
    users = graph_client.get('{0}/users'.format(graph_url)).json()
    return users['value'] if 'value' in users else []

def get_group_users(token, groupid):
    graph_client = OAuth2Session(token=token)
    users = graph_client.get('{0}/groups/{1}/members'.format(graph_url, groupid)).json()
    return users['value'] if 'value' in users else []

def get_user_meetings(token, userid):
    headers = _get_request_heads(token)
    headers['path'] = '/Skype.Analytics/Users(\'{0}\')/Communications?%24top=500'.format(userid)
    headers['referer'] = 'https://admin.teams.microsoft.com/users/{0}/activity'.format(userid)

    uri = 'https://api.interfaces.records.teams.microsoft.com/Skype.Analytics/Users(\'{0}\')/Communications?%24top=500'.format(userid)
    r = requests.get(uri, headers=headers)
    result = r.json()

    return result['value'] if 'value' in result else []

def get_meeting_records(token, userid, meetingid):
    headers = _get_request_heads(token)
    headers['path'] = '/Skype.Analytics/Communications(\'{0}\')/Participants'.format(meetingid)
    headers['referer'] = 'https://admin.teams.microsoft.com/users/{0}/meeting/{1}'.format(userid, meetingid)

    uri = 'https://api.interfaces.records.teams.microsoft.com/Skype.Analytics/Communications(\'{0}\')/Participants'.format(meetingid)
    r = requests.get(uri, headers=headers)
    result = r.json()

    return result['value'] if 'value' in result else []
