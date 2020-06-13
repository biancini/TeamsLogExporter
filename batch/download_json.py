import requests
import json
import csv
import sys
import os.path
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from urllib import parse
from datetime import datetime, time

'''
Scaricare i dati dal report creato appostivamente qui:
https://cqd.teams.microsoft.com/spd/#/Dashboard?language=it-IT
'''


def download_call_data(t, call_id):
    if os.path.isfile(f'json/{call_id}.json'):
        return 0
        
    uri = f'https://graph.microsoft.com/beta/communications/callRecords/{call_id}?$expand=sessions($expand=segments)'
    head = { 'Authorization': f'Bearer {t}' }
    r = requests.get(uri, headers=head)
    response = r.json()

    if 'error' in response:
        print (f'{response}')
        return 0
    else:
        with open('json/{0}.json'.format(call_id), 'w') as outfile:
            outfile.write(json.dumps(response, indent=4))
            outfile.close()

        return 1


if __name__ == '__main__':
    tenant_id = os.getenv('TENANTID_ENAIP', None)
    client_id = os.getenv('APPID_ENAIP', None)
    client_secret =  os.getenv('APPSECRET_ENAIP', None)
    num_threads = 10

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

    filename = 'calls.csv'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    print(f'Reading data from file {filename}')

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
                if call_id == "Conference Id": continue
                future = pool.submit(download_call_data, t, call_id)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

            for future in futures:
                result = future.result()
                out += result
        
    print(f'Script finito, scaricati {out} files.')