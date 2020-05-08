import glob
import shutil
from datetime import datetime
from os import path, remove
from openpyxl import load_workbook

base = "D:\Fondazione Enaip Lombardia\Didattica a Distanza - Report meeting Teams"
#base = "D:\OneDrive\Documenti\work\enaip\Formazione a Distanza\Strumenti Teams\Report meeting Teams"
files = [f for f in glob.glob("excel/**/*.xlsx", recursive=True)]

folders = {
    datetime(2020, 4, 5): '04_Report Teams 30mar_3apr',
    datetime(2020, 4, 12): '05_Report Teams 6-10 apr-20',
    datetime(2020, 4, 19): '06_Report Teams 14-17 apr-20',
    datetime(2020, 4, 26): '07_Report Teams 20-24 apr-20',
    datetime(2020, 5, 3): '08_Report Teams 27-30 apr-20'
}

total_files = len(files)
file_moved = 0

for f in files:
    file_date = datetime.strptime(path.basename(f)[:10], '%Y-%m-%d')
    
    for key, value in folders.items():
        if file_date <= key:
            newpath = path.join(base, value, path.basename(f))
            #print (f'mv {f} {newpath}')
            shutil.copy(f, newpath)
            file_moved = file_moved + 1
            break

print(f'Total files {total_files}')
print(f'Files moved {file_moved}')

print("Script finito.")