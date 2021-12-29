import requests
import shutil
import sys
import getopt
import configparser
from glob import glob
from datetime import datetime
from os import path, makedirs, chdir
from utils import get_access_token, allsundays, nearestsunday


def get_graph_data(t, uri):
    while uri:
        head = { 'Authorization': f'Bearer {t}' }
        r = requests.get(uri, headers=head)
        response = r.json()

        if 'error' in response:
            raise Exception(f'{response}')

        yield from response['value']
        uri = response['@odata.nextLink'] if '@odata.nextLink' in response else None


def _get_people(configuration):
    ente = configuration['ente']
    t = get_access_token(ente)

    groups = []
    uri = 'https://graph.microsoft.com/beta/groups?$orderby=displayName'
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

    return people


def divide_excel(configuration):
    local = configuration['local'] == 'true'
    base = configuration['basepath']

    lookdir = '.'
    if local:
        chdir(base)
        lookdir = configuration['xllookdir']

    folders = []
    for d in allsundays([2020, 2021, 2022]):
        folders.append(d)

    people = _get_people(configuration)

    files = glob(f'{lookdir}/**/*.xlsx', recursive=True)
    total_files = len(files)
    file_moved = 0

    for f in files:
        centro = '00_Generale'
        for c, o in people.items():
            for organizer in o:
                if organizer in path.basename(f):
                    centro = c

        file_date = datetime.strptime(path.basename(f)[:10], '%Y-%m-%d')
        
        for d in folders:
            folder = '%s_Report Teams' % d.strftime("%Y-%m-%d")

            if file_date <= d:
                newpath = path.join(base, centro, 'Report FAD', folder)

                if not path.exists(newpath):
                    makedirs(newpath)
                
                newpath = path.join(newpath, path.basename(f))
                if f not in newpath:
                    shutil.move(f, newpath)
                    file_moved = file_moved + 1

                break

    return total_files, file_moved


def divide_zipfile(configuration):
    zipfilename = configuration['zipfile']

    zipfolder = path.join(configuration['basepath'], configuration['zipfolder'])
    zippath = path.join(zipfolder, zipfilename)

    if path.exists(zippath):
        return None

    shutil.move(zipfilename, zippath)
    return zipfolder


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini', encoding='utf-8')
    ente = 'ENAIP'
    local = 'false'
    zipfilename = '%s_Report.zip' % nearestsunday().strftime("%Y-%m-%d")

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"he:lz:", ["help", "ente=", "local", "zipfile="])
    except getopt.GetoptError:
        print('divide_excel.py [-e <ente>] [-l] [-z <zipfile>]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('divide_excel.py [-e <ente>] [-l] [-z <zipfile>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        elif o in ('-l', '--local'):
            local = 'true'
        elif o in ('-z', '--zipfile'):
            zipfilename = a
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente
    configuration['local'] = local
    configuration['zipfile'] = zipfilename

    print(f'Working for institution {ente}. Working on %s source.' % ('local' if local else 'remote'))

    total_files, file_moved = divide_excel(configuration)
    print(f'Total excel files {total_files}.')
    print(f'Files excel moved {file_moved}.')

    moved = divide_zipfile(configuration)
    if moved is None:
        print('Zipfile already present, not moving.')
    else:
        print(f'Moved zipped file to folder {moved}.')
        
    print("Script finito.")