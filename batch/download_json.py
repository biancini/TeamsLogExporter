import requests
import json
import csv
import sys
import os.path
import threading
import tqdm
from urllib import parse
from datetime import datetime, time
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

'''
Scaricare i dati dal report creato appostivamente qui:
https://cqd.teams.microsoft.com/spd/#/Dashboard?language=it-IT
'''


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def download_call_data(t, call_ids):
    for call_id in tqdm.tqdm(call_ids):
        #print("Getting data for call id %s" % call_id)
        if os.path.isfile('json/{0}.json'.format(call_id)):
            continue

        uri = 'https://graph.microsoft.com/beta/communications/callRecords/{0}?$expand=sessions($expand=segments)'.format(call_id)
        head = { 'Authorization': 'Bearer {0}'.format(t) }
        r = requests.get(uri, headers=head)
        response = r.json()

        if 'error' in response:
            print ("%s" % response)
        else:
            #print ("Saved in JSON file.")
            with open('json/{0}.json'.format(call_id), 'w') as outfile:
                json.dump(response, outfile)


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

print("Reading data from file %s" % filename)

call_ids = []
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        call_id = row[0]
        call_ids.append(call_id)

call_ids = list(split(call_ids, num_threads))
threads = []
for thid in range(num_threads):
    th = threading.Thread(name='non-blocking', target=download_call_data, args=(t, call_ids[thid]))
    threads.append(th)
    th.start()

for th in threads:
    th.join()

print("Script finito.")