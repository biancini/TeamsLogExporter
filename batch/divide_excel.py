import glob
from os import path, rename, mkdir
from openpyxl import load_workbook

files = [f for f in glob.glob("excel/**/*.xlsx", recursive=True)]

total_files = len(files)
file_moved = 0
file_error = 0

for f in files:
    try:
        workbook = load_workbook(f)
        worksheet = workbook['Registro']

        row_count = worksheet.max_row
        if row_count <= 2:
            if not path.isdir(path.join(path.dirname(f), 'Altre Riunioni')):
                mkdir(path.dirname(f), 'Altre Riunioni')
            to_path = path.join(path.dirname(f), 'Altre Riunioni', path.basename(f))
            rename(f, to_path)
            file_moved += 1
    except:
        file_error += 1

print(f'Total files {total_files}')
print(f'Files moved {file_moved}')
print(f'Files with errors {file_error}')

print("Script finito.")