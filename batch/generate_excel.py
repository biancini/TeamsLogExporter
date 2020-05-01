
import requests
import json
import glob
import csv
import sys
import os.path
import threading
import math
from urllib import parse
from datetime import datetime, time
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter


usernames = {}


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def get_usernamefromid(t, userid):
    if userid == 'Sconosciuto': return 'Sconosciuto'

    if userid not in usernames:
        uri = 'https://graph.microsoft.com/beta/users/{0}'.format(userid)
        head = { 'Authorization': 'Bearer {0}'.format(t) }
        r = requests.get(uri, headers=head)
        user = r.json()
        if 'displayName' in user:
            usernames[userid] = user['displayName']
        else:
            usernames[userid] = 'Sconosciuto (%s)' % userid

    return usernames[userid]


def generate_excel(t, list_files):
    for filename in list_files:
        with open(filename) as json_file:
            p = json.load(json_file)

            name = 'Sconosciuto'
            if 'organizer' in p and p['organizer'] is not None:
                if 'user' in p['organizer'] and p['organizer']['user'] is not None:
                    if 'id' in p['organizer']['user']:
                        name = get_usernamefromid(t, p['organizer']['user']['id'])

            start_time = datetime.strptime(p['startDateTime'].split('.', 1)[0].split('Z', 1)[0], '%Y-%m-%dT%H:%M:%S')
            start_time = start_time.strftime('%Y-%m-%d %H:%M')
            dest_filename = "excel/%s - %s.xlsx" % (start_time, name)

            if os.path.isfile(dest_filename):
                os.remove(filename)
                continue

            users = {}
            for c in p['sessions']:
                if 'caller' not in c or c['caller'] is None:
                    continue
                if 'identity' not in c['caller'] or c['caller']['identity'] is None:
                    continue
                if 'user' not in c['caller']['identity'] or c['caller']['identity']['user'] is None:
                    continue
                if 'id' not in c['caller']['identity']['user'] or c['caller']['identity']['user']['id'] is None:
                    continue

                curuid = c['caller']['identity']['user']['id']
                if curuid not in users:
                    displayname = get_usernamefromid(t, curuid)
                    users[curuid] = { 'name': displayname, 'min_start': None, 'max_end': None, 'duration': 0 }

                start = datetime.strptime(c['startDateTime'].split('.', 1)[0].split('Z', 1)[0], '%Y-%m-%dT%H:%M:%S')
                if users[curuid]['min_start'] is None or start < users[curuid]['min_start']:
                    users[curuid]['min_start'] = start

                end = datetime.strptime(c['endDateTime'].split('.', 1)[0].split('Z', 1)[0], '%Y-%m-%dT%H:%M:%S')
                if users[curuid]['max_end'] is None or end > users[curuid]['max_end']:
                    users[curuid]['max_end'] = end
                
                if end is not None and start is not None:
                    delta = end - start
                    users[curuid]['duration'] += delta.seconds

            participants = []
            for _uid, data in users.items():
                data['duration'] /= 60
                hours = math.floor(data['duration'] / 60)
                minutes = math.floor(data['duration'] % 60)
                duration = "{0} ore e {1} minuti".format(hours, minutes)

                participants.append({ 'uid': _uid, 'name': data['name'], 'start': data['min_start'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'end': data['max_end'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'duration': duration})

            ###########

            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = 'Registro'

            worksheet.append(['Partecipante', 'Inizio presenza', 'Fine presenza', 'Tempo di partecipazione'])
            for cell in worksheet["1:1"]:
                cell.font = Font(bold=True)

            i = 1
            for pp in participants:
                i = i + 1

                duration = pp['duration'].replace(" ore e ", ":").replace(" minuti", "").split(":")
                worksheet.append([
                    pp['name'],
                    datetime.strptime(pp['start'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S'),
                    datetime.strptime(pp['end'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S'),
                    time(int(duration[0]), int(duration[1]), 0)
                ])

                cell = worksheet.cell(i, 2)
                cell.number_format = 'dd/mm/yyyy hh:mm'
                cell = worksheet.cell(i, 3)
                cell.number_format = 'dd/mm/yyyy hh:mm' 
                cell = worksheet.cell(i, 4)
                cell.number_format = 'h "ore e" mm "minuti"' 

            mediumStyle = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
            worksheet.add_table(Table(ref='A1:D%s'%i, displayName='RegistroPresenze', tableStyleInfo=mediumStyle))
            worksheet.sheet_view.showGridLines = False

            column_widths = [30, 20, 20, 20]
            for i, column_width in enumerate(column_widths):
                worksheet.column_dimensions[get_column_letter(i+1)].width = column_width

            workbook.save(filename=dest_filename)
    
        os.remove(filename)


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
r = requests.post(uri, data = data)
t = r.json()['access_token']

num_threads = 10
json_files = glob.glob("json/*.json")
json_files = list(split(json_files, num_threads))

threads = []
for thid in range(num_threads):
    th = threading.Thread(name='non-blocking', target=generate_excel, args=(t, json_files[thid]))
    threads.append(th)
    th.start()

for th in threads:
    th.join()

print("Script finito.")