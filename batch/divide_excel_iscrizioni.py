from datetime import datetime
from os import chdir
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

reportfad = True
#base = 'D:\Fondazione Enaip Lombardia\Pianificazione Attività - Documenti'
base = '/Users/andrea/Fondazione Enaip Lombardia/Istruzione e Formazione Professionale - Anno Scolastico 2020 2021/Iscrizioni'
chdir(base)

excel_file = '/Users/andrea/Downloads/Iscrizioni corsi IeFP - Istruzione e Formazione Professionale_Anno Formativo 2020_2021.xlsx'
nome_excel = 'Iscritti 15-21giu 20.xlsx'
data_da = datetime(2020, 6, 15)
data_a = datetime(2020, 6, 21)

centri = {
    'Bergamo': 'Bergamo',
    'Busto Arsizio': 'Busto Arsizio',
    'Cantù': 'Cantù',
    'Como': 'Como',
    'Cremona': 'Cremona',
    'Dalmine': 'Dalmine',
    'Lecco': 'Lecco',
    'Magenta': 'Magenta',
    'Mantova': 'Mantova',
    'Melzo': 'Melzo',
    'Milano Giacinti': 'Milano Giacinti',
    'Monticello': 'Monticello',
    'Morbegno': 'Morbegno',
    'Pavia': 'Pavia',
    'Romano': 'Romano',
    'Varese': 'Varese',
    'Vigevano': 'Vigevano',
    'Vimercate': 'Vimercate',
    'Voghera': 'Voghera'
}

wb = load_workbook(filename=excel_file)
ws = wb['Form1']

for c, cc in centri.items():
    new_wb = Workbook()
    new_ws = new_wb.active
    new_ws.title = 'Form1'

    count = 0
    for row in ws.iter_rows():
        data_iscrizione = row[2].value
        sede = row[26].value

        if data_iscrizione == 'Ora di completamento':
            new_ws.append([r.value for r in row])
            continue

        if sede != cc:
            continue

        if not isinstance(data_iscrizione, datetime):
            continue
        
        if data_iscrizione < data_da or data_iscrizione > data_a:
            continue
        
        new_ws.append([r.value for r in row])
        count += 1

    mediumStyle = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
    new_ws.add_table(Table(ref=f'A1:DA{count+1}', displayName='RegistroPresenze', tableStyleInfo=mediumStyle))

    newpath = f'{base}/Schede Iscrizione/{c}/{nome_excel}'
    new_wb.save(filename=newpath)
    new_wb.close()

    print(f'Generato il file per {c} con {count} iscritti')

print("Script finito.")