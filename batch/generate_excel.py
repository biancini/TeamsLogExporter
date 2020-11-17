
import requests
import json
import glob
import os.path
import math
import sys
import getopt
import configparser
from tqdm import tqdm
from dateutil import tz
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

from .utils import get_access_token


usernames = {}
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Rome')


def get_usernamefromid(t, userid, displayName=False):
    if userid == 'Sconosciuto': return 'Sconosciuto'

    keyname = userid
    username = f'Sconosciuto ({userid})'
    if displayName:
        keyname = f'{keyname}_d'

    if keyname not in usernames:
        uri = f'https://graph.microsoft.com/beta/users/{userid}'
        head = { 'Authorization': f'Bearer {t}' }
        r = requests.get(uri, headers=head)
        user = r.json()


        if displayName:
            if 'displayName' in user:
                usernames[keyname] = user['displayName']
            else:
                usernames[keyname] = username
        else:   
            if 'surname' in user and 'givenName' in user:            
                usernames[keyname] = f'{user["surname"]} {user["givenName"]}'
            else:
                usernames[keyname] = username

    return usernames[keyname]


def generate_excel_file(t, filename):
    with open(filename) as json_file:
        p = json.load(json_file)

        name = 'Sconosciuto'
        if 'organizer' in p and p['organizer'] is not None:
            if 'user' in p['organizer'] and p['organizer']['user'] is not None:
                if 'id' in p['organizer']['user']:
                    name = get_usernamefromid(t, p['organizer']['user']['id'], True)

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

            if 'userAgent' in c['caller'] and 'headerValue' in c['caller']['userAgent'] and c['caller']['userAgent']['headerValue'] == 'SkypeBot Call Recorder Teams':
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

        if len(participants) <= 1:
            json_file.close()
            return 0

        participants.sort(key=lambda stud: 'zzz_{}'.format(stud['name']) if 'Sconosciuto' in stud['name'] else stud['name'] )

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

        report_id = os.path.basename(filename).replace('.json', '')
        worksheet.append([f''])
        worksheet.append([f'Report generato per il meeting con ID: {report_id}'])

        column_widths = [30, 20, 20, 20]
        for i, column_width in enumerate(column_widths):
            worksheet.column_dimensions[get_column_letter(i+1)].width = column_width

        workbook.save(filename=dest_filename)

    json_file.close()
    #os.remove(filename)
    return 1


def generate_excel(configuration):
    ente = configuration['ente']
    t = get_access_token(ente)

    json_files = glob.glob("json/*.json")
    out = 0
    num_threads = 10

    with ProcessPoolExecutor(max_workers=num_threads) as pool:
        with tqdm(total=len(json_files)) as progress:
            futures = []
            for filename in json_files:
                future = pool.submit(generate_excel_file, t, filename)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)

            for future in futures:
                result = future.result()
                out += result
        
    print(f'Created {out} excel files.')
    return out


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    ente = 'ENAIP'

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"he:", ["help", "ente="])
    except getopt.GetoptError:
        print('generate_excel.py [-e <ente>]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('download_json.py [-e <ente>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente

    generate_excel(configuration)
    print("Script finito.")