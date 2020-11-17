import requests
import shutil
import sys
import getopt
import configparser
from glob import glob
from datetime import datetime, date, timedelta
from os import path, makedirs, chdir
from urllib import parse

from .utils import get_access_token, allsundays


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


def divide_excel(configuration):
    ente = configuration['ente']
    local = configuration['local']
    base = configuration['basepath']
    t = get_access_token(ente)

    print(f'Working for institution {ente}. Working on %s source.' % ('local' if local else 'remote'))

    reportfad = True
    lookdir = '.'

    if local:
        chdir(base)
        lookdir = configuration['xllookdir']

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
                    shutil.move(f, newpath)
                    file_moved = file_moved + 1

                break

    print(f'Total excel files {total_files}')
    print(f'Files excel moved {file_moved}')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    ente = 'ENAIP'
    local = False

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"he:l", ["help", "ente=", "local"])
    except getopt.GetoptError:
        print('divide_excel.py [-e <ente>] [-l]')
        sys.exit(2)
    
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

    configuration = config[ente]
    configuration['ente'] = ente
    configuration['local'] = local

    divide_excel(configuration)
    print("Script finito.")