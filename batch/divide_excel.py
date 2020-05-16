import shutil
from glob import glob
from datetime import datetime
from os import path, remove, makedirs, chdir
from openpyxl import load_workbook

reportfad = True
#base = 'D:\Fondazione Enaip Lombardia\Didattica a Distanza - Report meeting Teams'
base = 'D:\Fondazione Enaip Lombardia\Pianificazione Attività - Documenti'
#chdir(base)
files = glob('./**/*.xlsx', recursive=True)

folders = {
    datetime(2020, 4, 5): '04_Report Teams 30mar_3apr',
    datetime(2020, 4, 12): '05_Report Teams 6-10 apr-20',
    datetime(2020, 4, 19): '06_Report Teams 14-17 apr-20',
    datetime(2020, 4, 26): '07_Report Teams 20-24 apr-20',
    datetime(2020, 5, 3): '08_Report Teams 27-30 apr-20',
    datetime(2020, 5, 10): '09_Report Teams 4-8 mag-20',
    datetime(2020, 5, 17): '10_Report Teams 11-15 mag-20'
}

people = {
    'Bergamo': [
        'Adriano Fico', 'Arianna Assandri', 'Lucia Manuela Dondossola',
        'Arianna Assandri', 'Gianalberto Lubrina', 'Giacomo Suardi',
        'Nicola Iannone', 'Serena Roveri', 'Matteo Rossi',
        'Stella Galbiati', 'Enrico Caroppo', 'Daphne Della Vite',
        'Pippo Grossi', 'Enrico Canali', 'Chiara Tiraboschi',
        'Giacomo Scandola', 'Elena Rottigni', 'Fabio Mazzoleni',
        'Diego Pagnoncelli', 'Clara Mangili', 'Enrico Caroppo',
        'Emiliano Amadei', 'Elena Besola', 'Michela Vezzoli',
        'Angela Macario', 'Lorenzo Pezzotti', 'Lidia Gherardi',
        'Chiara Martinelli', 'Cecilia Acerbi', 'Laiza Ratti',
        'Gabriella Erba'
    ],
    'Bergamo ITS': [
        'Valentina Iavarone', 'Ramona Ubbiali', 'Giacomo Scandola',
        'Marcello Cenati'
    ],
    'Botticino': [ 'Daniela Melardi' ],
    'Busto Arsizio': [
        'Raffaello Vaghi', 'Chiara Ferrè', 'Donata Molon', 'Paolo Zuffinetti',
        'Paola Zerbi', 'Michele Della Valle', 'Francesca Milani', 'Raffaella Pigoli',
        'Laura Ferioli', 'Franca Guarracino'
    ],
    'Cantu': [ 'Viviana Tucci', 'Matteo Roncoroni', 'Federica Meroni' ],
    'Como': [
        'Cortellezzi Arianna', 'Bernasconi Sandra', 'Oricchio Mauro',
        'Clerici Rossella', 'Bianchi Anna Maria', 'Beretta Francesco',
        'Morselli Roberto', 'Colombo Manuela',  'Garbi Miriam'
    ],
    'Cremona': [
        'Elidoro Claudio', 'Laura Blasutta',
        #####
        'Granelli Silvia', 'Bignami Mariarosa',
        'Fiori Enrico Angelo', 'Bellocchio Matteo', 'Biolchi Federico',
        'Bonoli Michele', 'Benedetti Stefano', 'Galli Giorgio',
        'Maccagnola Daniela', 'Mignani Paola', 'Nicolazzo Sabrina',
        'Oliani Donatella', 'Platè Enrico', 'Portesani Simone',
        'Riccardi Daniela', 'Somenzini Marzia', 'Valcarenghi Mario Attilio'
    ],
    'Dalmine': [
        'Chiara Pezzotta', 'Maurizio Gavina', 'Debora Stignani',
        'Laura Trombini', 'Chiara Nicoli', 'Nadia Dalla Longa'
    ],
    'Lecco': [ 'Federica Colombo' ],
    'Magenta': [ 'Laura Cuzzocrea' ],
    'Mantova': [ 'Elvira Morandi Gadioli', 'Fabio Veneri' ],
    'Melzo': [ 'Alessandro Arbitrio' ],
    'Monticello': ['Alberta Molinari', 'Stefania Sala' ],
    'Morbegno': [ 'Donatella Caelli', 'Jiji Bezi', 'Claudia Del Barba' ],
    'Pavia': [
        'Corsico Giovanni', 'Bernorio Viviana', 'Casella Massimo',
        'Belli Alessandro', 'Susino Giovanni', 'Passarella Chantall',
        'Ferraris Andrea', 'Saronni Catia', 'Longhi Daniele'
    ],
    'Romano': [ 'Annamaria Bergamini' ],
    'Varese': [
        'Alessandro Bertoni', 'Diana Accili', 'Chiara Roncari', 
        'Sara Campiglio', 'Domenico Battista', 'Simone Porta',
        'Donatella Gelmi'
    ],
    'Vigevano': [ 'Margherita Previde Massara', 'Viola Donato' ],
    'Vimercate': [ 'Davide Panzeri', 'Jacopo Tonon' ],
    'Voghera': [ 'Alessandro Belli', 'Fabio Faroldi' ]
}

total_files = len(files)
file_moved = 0

for f in files:
    centro = '00_Generale' if reportfad else 'Altro'
    for c, o in people.items():
        for organizer in o:
            if organizer in path.basename(f):
                centro = c

    file_date = datetime.strptime(path.basename(f)[:10], '%Y-%m-%d')
    
    for d, folder in folders.items():
        if file_date <= d:
            if reportfad:
                newpath = path.join(base, centro, 'Report FAD', folder)
            else:
                newpath = path.join(base, centro, folder)

            if not path.exists(newpath):
                makedirs(newpath)
            
            newpath = path.join(newpath, path.basename(f))
            #print (f'mv {f} {newpath}')
            shutil.copy(f, newpath)
            file_moved = file_moved + 1

            break

print(f'Total files {total_files}')
print(f'Files moved {file_moved}')

print("Script finito.")