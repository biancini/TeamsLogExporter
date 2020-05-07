
import requests
import json
import glob
import os.path
import math
from tqdm import tqdm
from dateutil import tz
from urllib import parse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, time, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter


usernames = {}
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Rome')


def get_usernamefromid(t, userid):
    if userid == 'Sconosciuto': return 'Sconosciuto'

    if userid not in usernames:
        uri = f'https://graph.microsoft.com/beta/users/{userid}'
        head = { 'Authorization': f'Bearer {t}' }
        r = requests.get(uri, headers=head)
        user = r.json()
        if 'displayName' in user:
            usernames[userid] = user['displayName']
        else:
            usernames[userid] = f'Sconosciuto ({userid})'

    return usernames[userid]


def generate_excel(t, filename):
    with open(filename) as json_file:
        p = json.load(json_file)

        name = 'Sconosciuto'
        if 'organizer' in p and p['organizer'] is not None:
            if 'user' in p['organizer'] and p['organizer']['user'] is not None:
                if 'id' in p['organizer']['user']:
                    name = get_usernamefromid(t, p['organizer']['user']['id'])

        start_time = datetime.strptime(p['startDateTime'].split('.', 1)[0].split('Z', 1)[0], '%Y-%m-%dT%H:%M:%S')
        start_time = start_time.replace(tzinfo=from_zone).astimezone(to_zone)
        start_time = start_time.strftime('%Y-%m-%d %H-%M')
        dest_filename = f'excel/{start_time} - {name}.xlsx'

        i = 2
        while os.path.isfile(dest_filename):
            dest_filename = f'excel/{start_time} - {name} - {i}.xlsx'
            i = i + 1

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
            start = start.replace(tzinfo=from_zone).astimezone(to_zone)
            if users[curuid]['min_start'] is None or start < users[curuid]['min_start']:
                users[curuid]['min_start'] = start

            end = datetime.strptime(c['endDateTime'].split('.', 1)[0].split('Z', 1)[0], '%Y-%m-%dT%H:%M:%S')
            end = end.replace(tzinfo=from_zone).astimezone(to_zone)
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

            start = datetime.strptime(pp['start'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(pp['end'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')

            delta = (end - start).seconds
            delta /= 60*60*24

            worksheet.append([
                pp['name'],
                start,
                end,
                delta
            ])

            cell = worksheet.cell(i, 2)
            cell.number_format = 'dd/mm/yyyy hh:mm'
            cell = worksheet.cell(i, 3)
            cell.number_format = 'dd/mm/yyyy hh:mm' 
            cell = worksheet.cell(i, 4)
            cell.number_format = 'h "ore e" mm "minuti"' 

        mediumStyle = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
        worksheet.add_table(Table(ref=f'A1:D{i}', displayName='RegistroPresenze', tableStyleInfo=mediumStyle))
        worksheet.sheet_view.showGridLines = False

        column_widths = [30, 20, 20, 20]
        for i, column_width in enumerate(column_widths):
            worksheet.column_dimensions[get_column_letter(i+1)].width = column_width

        workbook.save(filename=dest_filename)

    json_file.close()
    #os.remove(filename)
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

    uri = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    r = requests.post(uri, data=data).json()

    if not 'access_token' in r:
        print(f'{r}')
        exit(1)

    t = r['access_token']

    num_threads = 10
    json_files = glob.glob("json/*.json")

    out = 0
    with ProcessPoolExecutor(max_workers=num_threads) as pool:
        with tqdm(total=len(json_files)) as progress:
            futures = []
            for filename in json_files:
                future = pool.submit(generate_excel, t, filename)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

            for future in futures:
                result = future.result()
                out += result
        
    print(f'Script finito, creati {out} files.')