import requests
import shutil
import sys
import getopt
from glob import glob
from datetime import datetime, date, timedelta
from os import path, makedirs, chdir, getenv
from urllib import parse


def get_access_token(ente):
    tenant_id = getenv(f'TENANTID_{ente}', None)
    client_id = getenv(f'APPID_{ente}', None)
    client_secret =  getenv(f'APPSECRET_{ente}', None)

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


def allsundays(years):
    for year in years:
        d = datetime(year, 1, 1)                # January 1st
        d += timedelta(days = 6 - d.weekday())  # First Sunday
        while d.year == year:
            yield d
            d += timedelta(days = 7)


def get_graph_data(t, uri):
    while uri:
        head = { 'Authorization': f'Bearer {t}' }
        r = requests.get(uri, headers=head)
        response = r.json()

        if 'error' in response:
            print (f'{response}')
            sys.exit(1)

        yield from response['value']
        uri = response['@odata.nextLink'] if '@odata.nextLink' in response else None


def main(argv):
    try:
        opts, _ = getopt.getopt(argv,"he:l", ["help", "ente=", "local"])
    except getopt.GetoptError:
        print('divide_excel.py [-e <ente>] [-l]')
        sys.exit(2)

    ente = 'ENAIP'
    local = False
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('download_json.py [-e <ente>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        elif o in ('-l', '--local'):
            local = True
        else:
            assert False

    t = get_access_token(ente)

    print(f'Working for institution {ente}. Working on %s source.' % ('local' if local else 'remote'))

    reportfad = True
    base = '/Users/andrea/Fondazione Enaip Lombardia/Pianificazione Attività - Documenti/Anno Formativo 2020-2021/'
    lookdir = '.'

    if local:
        chdir(base)
        lookdir = '00_Generale/Report FAD/'

    folders = []
    files = glob(f'{lookdir}/**/*.xlsx', recursive=True)
    for d in allsundays([2020, 2021]):
        folders.append(d)

    groups = []
    uri = f'https://graph.microsoft.com/beta/groups?$orderby=displayName'
    for g in get_graph_data(t, uri):
        groups.append(g)
    
    people = {}
    for g in groups:
        if g['displayName'].startswith('Organizzatori FAD '):
            centro = g['displayName'].replace('Organizzatori FAD ', '')
            groupid = g['id']

            participants = []
            uri = f'https://graph.microsoft.com/beta/groups/{groupid}/members'
            for p in get_graph_data(t, uri):
                participants.append(p['displayName'])

            people[centro] = participants

    total_files = len(files)
    file_moved = 0

    for f in files:
        centro = '00_Generale' if reportfad else 'Altro'
        for c, o in people.items():
            for organizer in o:
                if organizer in path.basename(f):
                    centro = c

        file_date = datetime.strptime(path.basename(f)[:10], '%Y-%m-%d')
        
        for d in folders:
            folder = '%s_Report Teams' % d.strftime("%Y-%m-%d")

            if file_date <= d:
                if reportfad:
                    newpath = path.join(base, centro, 'Report FAD', folder)
                else:
                    newpath = path.join(base, centro, folder)

                if not path.exists(newpath):
                    makedirs(newpath)
                
                newpath = path.join(newpath, path.basename(f))
                if f not in newpath:
                    #print (f'mv {f} {newpath}')
                    shutil.move(f, newpath)
                    file_moved = file_moved + 1

                break

    print(f'Total files {total_files}')
    print(f'Files moved {file_moved}')

    print("Script finito.")


if __name__ == '__main__':
    main(sys.argv[1:])