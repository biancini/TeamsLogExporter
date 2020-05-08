import shutil
from glob import glob
from datetime import datetime
from os import path, remove, makedirs, chdir
from openpyxl import load_workbook

#base = 'D:\Fondazione Enaip Lombardia\Didattica a Distanza - Report meeting Teams'
base = 'D:\Fondazione Enaip Lombardia\Pianificazione Attività - Documenti'
#base = 'D:\OneDrive\Documenti\work\enaip\Formazione a Distanza\Strumenti Teams\Report meeting Teams'
chdir(base)
files = glob('**/*.xlsx', recursive=True)

folders = {
    datetime(2020, 4, 5): '04_Report Teams 30mar_3apr',
    datetime(2020, 4, 12): '05_Report Teams 6-10 apr-20',
    datetime(2020, 4, 19): '06_Report Teams 14-17 apr-20',
    datetime(2020, 4, 26): '07_Report Teams 20-24 apr-20',
    datetime(2020, 5, 3): '08_Report Teams 27-30 apr-20'
}

people = {
    'Bergamo': [],
    'Botticino': [ 'Daniela Melardi' ],
    'Busto Arsizio': [
        'Raffaello Vaghi', 'Chiara Ferrè', 'Donata Molon', 'Paolo Zuffinetti',
        'Paola Zerbi', 'Michele DellaValle', 'Francesca Milani', 'Raffaella Pigoli',
        'Laura Ferioli', 'Franca Guarracino'
    ],
    'Cantu': [ 'Viviana Tucci', 'Matteo Roncoroni', 'Federica Meroni' ],
    'Como': [
        'Arianna Cortellezzi', 'Sandra Bernasconi', 'Maura Oricchio',
        'Rossella Clerici', 'Ann Bianchi', 'Francesco Beretta',
        'Roberto Morselli', 'Manuela Colombo',  'Miriam Garbi'
    ],
    'Cremona': [
        'Claudio Elidoro', 'Silvia Granelli', 'Mariarosa Bignami',
        'Enrico Fiori', 'Matteo Bellocchio', 'Federico Biolchi',
        'Michele Bonoli', 'Stefano Benedetti', 'Giorgio Galli',
        'Daniela Maccagnola', 'Paola Mignani', 'Sabrina Nicolazzo',
        'Donatella Oliani', 'Enrico Platè', 'Simone Portesani',
        'Daniela Riccardi', 'Marzia Somenzini', 'Mario Valcarenghi'
    ],
    'Dalmine': [
        'Chiara Pezzotta', 'Maurizio Gavina', 'Debora Stignani',
        'Laura Trombini', 'Chiara Nicoli'
    ],
    'Lecco': [ 'Federica Colombo' ],
    'Magenta': [ 'Lara Cuzzocrea' ],
    'Mantova': [ 'Elvina Morandigadioli', 'Fabio Veneri' ],
    'Melzo': [ 'Alessandro Arbitrio' ],
    'Milano Giacinti': [ 'Nadia Dallalonga' ],
    'Monticello': ['Alberta Molinari', 'Stefania Sala' ],
    'Morbegno': [ 'Donatella Caelli', 'Jiji Bezi', 'Claudia Del Barba' ],
    'Pavia': [
        'Giovanni Corsico', 'Viviana Bernorio', 'Viviana Casella',
        'Alessandro Belli', 'Giovanni Susino', 'Chantall Passarella',
        'Andrea Ferraris', 'Catia Saronni', 'Daniele Longhi'
    ],
    'Romano': [ 'Anna Maria Bergamini' ],
    'Varese': [
        'Alessandro Bertoni', 'Diana Accili', 'Chiara Roncari', 
        'Sara Campiglio', 'Domenico Battista', 'Simone Porta',
        'Donatella Gelmi'
    ],
    'Vigevano': [ 'Margherita Previde', 'Viola Donato' ],
    'Vimercate': [ 'Davide Panzeri', 'Jacopo Tonon' ],
    'Voghera': [ 'Alessandro Belli', 'Fabio Faroldi' ]
}

total_files = len(files)
file_moved = 0

for f in files:
    centro = 'Altro'
    for c, o in people.items():
        for organizer in o:
            if organizer in path.basename(f):
                centro = c

    file_date = datetime.strptime(path.basename(f)[:10], '%Y-%m-%d')
    
    for d, folder in folders.items():
        if file_date <= d:
            newpath = path.join(base, centro, 'Report FAD', folder)
            if not path.exists(newpath):
                makedirs(newpath)
            
            newpath = path.join(newpath, path.basename(f))
            #print (f'mv {f} {newpath}')
            shutil.move(f, newpath)
            
            file_moved = file_moved + 1
            break

print(f'Total files {total_files}')
print(f'Files moved {file_moved}')

print("Script finito.")