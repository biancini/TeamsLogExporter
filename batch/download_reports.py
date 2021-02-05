import sys
import os
import getopt
import configparser
from glob import glob

from download_json import download_json, zip_jsonfiles
from generate_excel import generate_excel
from divide_excel import divide_excel


'''
Scaricare i dati dal report creato appostivamente qui:
https://cqd.teams.microsoft.com/spd/#/Dashboard?language=it-IT
'''


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    ente = 'ENAIP'
    filename = 'calls.csv'
    zipfilename = None

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "he:f:z:", ["help", "ente=", "file=", "zipfile="])
    except getopt.GetoptError:
        print('download_json.py [-e <ente>] [-f <file>] [-z <zipfile>]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('download_reports.py [-e <ente>] [-f <file>] [-z <zipfile>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        elif o in ('-f', '--file'):
            filename = a
        elif o in ('-z', '--zipfile'):
            zipfilename = a
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente
    if filename:
        configuration['filename'] = filename
    if zipfilename:
        configuration['zipfile'] = zipfilename
    configuration['local'] = 'false'

    print(f'Working for institution {ente}.')

    goon = True 
    numfiles = download_json(configuration)

    if numfiles <= 0:
        print('No files to be zipped.')
        goon = False

    if goon:
        zippedfiles = zip_jsonfiles(configuration)
    
        if numfiles != zippedfiles:
            print(f'Should have zipped {numfiles}, but zipped {zippedfiles}. Leaving json folder untouched.')
            goon = False

    if goon:
        numexcels = generate_excel(configuration)

        if numexcels <= 0:
            print("No excels generated.")
            goon = False

    if goon:
        moved = divide_excel(configuration)

        if moved <= 0:
            print("No files moved, preserving JSON file to check what happened...")
            goon = False

    if goon:
        basedir = 'json/'
        files = glob(f'{basedir}**/*.json', recursive=True)
        for f in files:
            os.remove(f)

    print("Script finito.")