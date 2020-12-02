
import requests
import json
import glob
import os.path
import sys
import getopt
import configparser
from tqdm import tqdm
from dateutil import tz
from operator import itemgetter
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

from utils import get_access_token


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


def generate_sheet_registro(worksheet, participants, filename):
    worksheet.append(['Partecipante', 'Inizio presenza', 'Fine presenza', 'Tempo di partecipazione'])
    for cell in worksheet["1:1"]:
        cell.font = Font(bold=True)

    i = 1
    for pp in participants:
        i = i + 1

        start = datetime.strptime(pp['start'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
        end = datetime.strptime(pp['end'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')

        delta = pp['duration']
        #delta = (end - start).seconds
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


def generate_sheet_partecipation(worksheet, participants, filename):
    titles = ['Partecipante']

    min_start = None
    cols = 0
    for pp in participants:
        start = datetime.strptime(pp['start'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
        start = start.replace(tzinfo=from_zone).astimezone(to_zone)
        if min_start is None or start < min_start:
            min_start = start

        le = len(pp['participation'])
        if le > cols:
            cols = le
    cols = int(cols/2)

    for ii in range(cols):
        titles.append(f'Inizio {ii}')
        titles.append(f'Fine {ii}')

    worksheet.append(titles)
    for cell in worksheet["1:1"]:
        cell.font = Font(bold=True)

    i = 1
    for pp in participants:
        i = i + 1
        
        values = [pp['name']]

        part = min_start
        for p in pp['participation']:
            d = (p - part).seconds
            d /= 60*60*24
            values.append(d)
            part = p

        worksheet.append(values)

        cell = worksheet.cell(i, 2)
        cell.number_format = 'dd/mm/yyyy hh:mm'
        for c in range(1, 1 + 2 * cols):
            cell = worksheet.cell(i, c + 1)
            cell.number_format = 'h "ore e" mm "minuti"' 

    report_id = os.path.basename(filename).replace('.json', '')
    worksheet.append([f''])
    worksheet.append([f'Report generato per il meeting con ID: {report_id}'])

    column_widths = [20 for _ in range(2 * cols + 1)]
    column_widths[0] = 30
    for ii, column_width in enumerate(column_widths):
        worksheet.column_dimensions[get_column_letter(ii+1)].width = column_width

    f = get_column_letter(1 + 2 * cols)
    mediumStyle = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
    worksheet.add_table(Table(ref=f'A1:{f}{i}', displayName='Partecipazione', tableStyleInfo=mediumStyle))
    worksheet.sheet_view.showGridLines = False

    # Generate Chart
    chart = BarChart()
    chart.type = "bar"
    chart.height = 20
    chart.width = 40
    chart.grouping = "stacked"
    chart.overlap = 100
    chart.legend = None
    chart.x_axis.scaling.orientation = "maxMin"

    for cur_col in range(2, 2 + 2 * cols):
        data = Reference(worksheet, min_col=cur_col, min_row=2, max_row=i, max_col=cur_col)
        cats = Reference(worksheet, min_col=1, min_row=2, max_row=i, max_col=1)
        chart.add_data(data, titles_from_data=False)
        chart.set_categories(cats)

    for ii, s in enumerate(chart.series):
        s.graphicalProperties.Shape3D = False
        if (ii % 2) == 0:
            s.graphicalProperties.line.noFill = True
            s.graphicalProperties.noFill = True
        else:
            s.graphicalProperties.line.solidFill = '5F8E28'
            s.graphicalProperties.solidFill = '5F8E28'
    
    worksheet.add_chart(chart, "A43")


def merge_times(times):
    times = iter(times)
    merged = next(times).copy()
    for entry in times:
        start, end = entry['start'], entry['end']
        if start <= merged['end']:
            # overlapping, merge
            merged['end'] = max(merged['end'], end)
        else:
            # distinct; yield merged and start a new copy
            yield merged
            merged = entry.copy()
    yield merged


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
            f = os.path.splitext(os.path.basename(filename))[0]
            wb_obj = load_workbook(dest_filename) 
            sheet_obj = wb_obj.active
            m_row = sheet_obj.max_row 
  
            for ii in range(1, m_row + 1): 
                cell_obj = sheet_obj.cell(row = ii, column = 1) 
                if cell_obj.value and f in cell_obj.value:
                    print(f'File excel already created for meetign with id {f}')
                    return 1

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
                if not 'participation' in users[curuid]: users[curuid]['participation'] = [] 

                users[curuid]['participation'].append({
                    'start': start.replace(tzinfo=from_zone).astimezone(to_zone),
                    'end': end.replace(tzinfo=from_zone).astimezone(to_zone)
                })

        participants = []
        for _uid, data in users.items():
            participation = sorted(data['participation'], key=itemgetter('start', 'end'))
            participation = merge_times(participation)

            duration = 0
            part = []
            for pp in participation:
                delta = pp['end'] - pp['start']
                duration += delta.seconds
                part.append(pp['start'])
                part.append(pp['end'])

            part.sort()
            participants.append({
                'uid': _uid,
                'name': data['name'],
                'start': data['min_start'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'end': data['max_end'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'duration': duration,
                'participation': part
            })

        if len(participants) <= 1:
            json_file.close()
            return 0

        participants.sort(key=lambda stud: 'zzz_{}'.format(stud['name']) if 'Sconosciuto' in stud['name'] else stud['name'] )

        ###########

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Registro'
        generate_sheet_registro(worksheet, participants, filename)
        worksheet = workbook.create_sheet('Partecipazione')
        generate_sheet_partecipation(worksheet, participants, filename)
        workbook.save(filename=dest_filename)

    json_file.close()
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
    
    if out > 0:
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

    filecount = generate_excel(configuration)
    print(f'Generati {filecount} file excel.')
    print("Script finito.")