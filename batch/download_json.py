import requests
import json
import csv
import sys
import getopt
import zipfile
import configparser
import os.path
from glob import glob
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

from utils import get_access_token, nearestsunday

'''
Scaricare i dati dal report creato appostivamente qui:
https://cqd.teams.microsoft.com/spd/#/Dashboard?language=it-IT
'''


def download_call_data(t, call_id):
    if os.path.isfile(f'json/{call_id}.json'):
        return 1
        
    uri = f'https://graph.microsoft.com/beta/communications/callRecords/{call_id}?$expand=sessions($expand=segments)'
    head = { 'Authorization': f'Bearer {t}' }
    r = requests.get(uri, headers=head)
    response = r.json()

    if 'error' not in response:
        with open('json/{0}.json'.format(call_id), 'w') as outfile:
            outfile.write(json.dumps(response, indent=4))
            outfile.close()

        return 1

    return 0


def download_json(configuration):
    ente = configuration['ente']
    filename = configuration['filename']
    t = get_access_token(ente)

    num_threads = 10
    call_ids = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            call_id = row[0]
            call_ids.append(call_id)

        csv_file.close()

    out = 0
    with ProcessPoolExecutor(max_workers=num_threads) as pool:
        with tqdm(total=len(call_ids)) as progress:
            futures = []
            for call_id in call_ids:
                if "Conference" in call_id: continue
                future = pool.submit(download_call_data, t, call_id)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

            for future in futures:
                result = future.result()
                out += result
        
    return out


def zip_jsonfiles(configuration):
    out = 0
    zipfilename = configuration['zipfile']
    
    if os.path.isfile(zipfilename):
        raise Exception(f'File zip {zipfilename} aleardy exists. Skipping zip file creation')

    zf = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
    basedir = 'json/'
    files = glob(f'{basedir}**/*.json', recursive=True)
    for f in files:
        zf.write(f, f.replace(basedir, ''))
        out += 1
    zf.close()
    return out


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    ente = 'ENAIP'
    filename = None
    zip = False
    zipfilename = '%s_Report.zip' % nearestsunday().strftime("%Y-%m-%d")

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "he:f:Zz:", ["help", "ente=", "file=", "zip", "zipfile="])
    except getopt.GetoptError:
        print('download_json.py [-e <ente>] [-f <file>] [-Z] [-z <zipfile>]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('download_json.py [-e <ente>] [-f <file>] [-Z] [-z <zipfile>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        elif o in ('-f', '--file'):
            filename = a
        elif o in ('-Z', '--zip'):
            zip = True
        elif o in ('-z', '--zipfile'):
            zip = True
            zipfilename = a
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente
    if filename:
        configuration['filename'] = filename
    if zipfilename:
        configuration['zipfile'] = zipfilename

    print(f'Working for institution {ente}.')
    print(f'Downloading all jsons for meeting listed in file {filename}.')
    numfiles = download_json(configuration)
    print(f'Finished downloading of json files, {numfiles} files downloaded.')

    if zip:
        if numfiles <= 0:
            print('No files to be zipped.')
        else:
            print(f'Zipping all JSON files in zip file {zipfilename}.')
            zippedfiles = zip_jsonfiles(configuration)
            print(f'Added {zippedfiles} files to zip.')
        
            if numfiles != zippedfiles:
                print(f'Should have zipped {numfiles}, but zipped {zippedfiles}. Leaving json folder untouched.')
    
    print("Script finito.")