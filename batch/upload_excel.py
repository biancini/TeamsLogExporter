import requests

import sys
import getopt
import configparser
import logging
from glob import glob
from datetime import datetime
from os import path, remove
from utils import get_access_token, get_user_credentials, allsundays, nearestsunday
from concurrent.futures import ProcessPoolExecutor
from office365.sharepoint.client_context import ClientContext


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


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


def upload_one_excel(configuration, f, people, folders):
    spbase = configuration['sharepointbase']
    sharepointlibrary = configuration['sharepointlibrary']
    spbase = configuration['sharepointbase']
    test_team_site_url = configuration['sharepointsite']
    sharepointlibrary = configuration['sharepointlibrary']

    cred = get_user_credentials()
    ctx = ClientContext(test_team_site_url).with_user_credentials(cred['username'], cred['password'])

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
                #remove(f)
                return target_file.serverRelativeUrl
                
            return None


def upload_excel(configuration):
    people = _get_people(configuration)
    
    lookdir = '.'
    folders = []
    files = glob(f'{lookdir}/**/*.xlsx', recursive=True)
    for d in allsundays([2020, 2021, 2022]):
        folders.append(d)

    total_files = len(files)
    file_uploaded = 0
    num_threads = 10
    
    with ProcessPoolExecutor(max_workers=num_threads) as pool:
        futures = []
        for f in files:
            future = pool.submit(upload_one_excel, configuration, f, people, folders)
            futures.append(future)

        for future in futures:
            result = future.result()
            if result is not None:
                file_uploaded += 1
                logging.info("(%d/%d) Uploaded file: %s", file_uploaded, total_files, result)
                

    return total_files, file_uploaded


def upload_zipfile(configuration):
    spbase = configuration['sharepointbase']
    test_team_site_url = configuration['sharepointsite']
    sharepointlibrary = configuration['sharepointlibrary']
    zipfolder = configuration['zipfolder']
    zipfilename = configuration['zipfile']

    cred = get_user_credentials()
    ctx = ClientContext(test_team_site_url).with_user_credentials(cred['username'], cred['password'])

    zippath = path.join(sharepointlibrary, spbase, zipfolder)
    target_folder = ctx.web.ensure_folder_path(zippath).execute_query()

    with open(zipfilename, 'rb') as content_file:
        file_content = content_file.read()

    name = path.basename(zipfilename)
    target_file = target_folder.upload_file(name, file_content).execute_query()
    
    return target_file.serverRelativeUrl if target_file else None


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini', encoding='utf-8')
    ente = 'ENAIP'
    zipfilename = '%s_Report.zip' % nearestsunday().strftime("%Y-%m-%d")

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"he:lz:", ["help", "ente=", "zipfile="])
    except getopt.GetoptError:
        print('upload_excel.py [-e <ente>] [-z <zipfile>]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('divide_excel.py [-e <ente>] [-z <zipfile>]')
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
    configuration['zipfile'] = zipfilename

    print(f'Working for institution {ente}.')

    total_files, file_uploaded = upload_excel(configuration)
    print(f'Total excel files {total_files}.')
    print(f'Files excel uploaded {file_uploaded}.')

    upload_zipfile(configuration)
    print("Script finito.")