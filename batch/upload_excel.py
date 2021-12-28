import requests
import shutil
import sys
import getopt
import configparser
from glob import glob
from datetime import datetime
from os import path

from office365.sharepoint.client_context import ClientContext

from utils import get_access_token, get_user_credentials, allsundays, nearestsunday


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


def upload_excel(configuration):
    ente = configuration['ente']
    spbase = configuration['sharepointbase']
    test_team_site_url = configuration['sharepointsite']
    sharepointlibrary = configuration['sharepointlibrary']

    t = get_access_token(ente)
    cred = get_user_credentials()
    ctx = ClientContext(test_team_site_url).with_user_credentials(cred['username'], cred['password'])

    print(f'Working for institution {ente}.')

    lookdir = '.'

    folders = []
    files = glob(f'{lookdir}/**/*.xlsx', recursive=True)
    for d in allsundays([2020, 2021, 2022]):
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
    file_uploaded = 0

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
                newpath = path.join(sharepointlibrary, spbase, centro, 'Report FAD', folder)
                target_folder = ctx.web.ensure_folder_path(newpath).execute_query()
                
                with open(f, 'rb') as content_file:
                    file_content = content_file.read()

                name = path.basename(f)
                target_file = target_folder.upload_file(name, file_content).execute_query()

                if target_file:
                    file_uploaded = file_uploaded + 1

    print(f'Total excel files {total_files}.')
    print(f'Files excel uploaded {file_uploaded}.')
    return file_uploaded


def upload_zipfile(configuration):
    spbase = configuration['sharepointbase']
    test_team_site_url = configuration['sharepointsite']
    sharepointlibrary = configuration['sharepointlibrary']
    zipfolder = configuration['zipfolder']

    if 'zipfile' in configuration:
        zipfilename = configuration['zipfile']
    else:
        s = nearestsunday()
        zipfilename = '%s_Report.zip' % s.strftime("%Y-%m-%d")

    cred = get_user_credentials()
    ctx = ClientContext(test_team_site_url).with_user_credentials(cred['username'], cred['password'])

    zippath = path.join(sharepointlibrary, spbase, zipfolder)
    target_folder = ctx.web.ensure_folder_path(zippath).execute_query()

    with open(zipfilename, 'rb') as content_file:
        file_content = content_file.read()

    name = path.basename(zipfilename)
    target_file = target_folder.upload_file(name, file_content).execute_query()

    if target_file:
        print('Uploaded zipped file to sharepoint.')
        return 1
    else:
        print('Error in loading zip file to sharpoint.')
        return 0


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini', encoding='utf-8')
    ente = 'ENAIP'

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"he:l", ["help", "ente="])
    except getopt.GetoptError:
        print('divide_excel.py [-e <ente>] [-l]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('divide_excel.py [-e <ente>] [-l]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente

    upload_excel(configuration)
    upload_zipfile(configuration)
    print("Script finito.")