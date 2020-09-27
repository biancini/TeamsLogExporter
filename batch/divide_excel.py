import shutil
from glob import glob
from datetime import datetime
from os import path, makedirs

reportfad = True
#base = 'D:\Fondazione Enaip Lombardia\Pianificazione Attività - Documenti\Anno Formativo 2020-2021'
base = '/Users/andrea/Fondazione Enaip Lombardia/Pianificazione Attività - Documenti/Anno Formativo 2020-2021/'
#chdir(base)
#lookdir = '00_Generale/Report FAD/'
lookdir = '.'
files = glob(f'{lookdir}/**/*.xlsx', recursive=True)

folders = [
    datetime(2020, 9,  6),
    datetime(2020, 9,  13),
    datetime(2020, 9,  20),
    datetime(2020, 9,  27),
]

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
        'Raffaello Vaghi', 'Chiara Ferrè', 'Donata Molon',
        'Paolo Zuffinetti', 'Paola Zerbi', 'Michele Della Valle',
        'Francesca Milani', 'Raffaella Pigoli', 'Laura Ferioli',
        'Franca Guarracino'
    ],
    'Cantù': [
        'Andrea Biotti', 'Viviana Tucci', 'Matteo Roncoroni',
        'Federica Meroni'
    ],
    'Como': [
        'Arianna Cortellezzi', 'Sandra Bernasconi', 'Mauro Oricchio',
        'Rossella Clerici', 'Anna Bianchi', 'Francesco Beretta',
        'Roberto Morselli', 'Manuela Colombo',  'Miriam Garbi',
        'Silvia Dellifiori', 'Adriano Drammissino', 'Laura Pellegatta'
    ],
    'Cremona': [
        'Claudio Elidoro', 'Laura Blasutta',
        #####
        'Silvia Granelli', 'Mariarosa Bignami',
        'Enrico Angelo Fiori ', 'Matteo Bellocchio', 'Federico Biolchi',
        'Michele Bonoli', 'Stefano Benedetti', 'Giorgio Galli',
        'Daniela Maccagnola', 'Paola Mignani', 'Sabrina Nicolazzo',
        'Donatella Oliani', 'Enrico Platè', 'Simone Portesani',
        'Daniela Riccardi', 'Marzia Somenzini', 'Mario Valcarenghi'
    ],
    'Dalmine': [
        'Chiara Pezzotta', 'Stefania Boschi', 'Laiza Ratti',
        'Clara Mangili'
    ],
    'Lecco': [
        'Federica Colombo', 'Beatrice  Pigolotti'
    ],
    'Magenta': [ 'Lara Cuzzocrea' ],
    'Mantova': [
        'Giovanna Maretti', 'Paolo Ghilotti', 'Antonella Bellini',
        'Fabio Veneri'
    ],
    'Melzo': [ 'Alessandro Arbitrio' ],
    'Milano Giacinti' : [
        'Maurizio Gavina', 'Debora Stignani', 'Laura Trombini',
        'Chiara Nicoli', 'Nadia Dallalonga', 'Domenico Scaldaferri'
    ],
    'Monticello': ['Alberta Molinari', 'Stefania Sala' ],
    'Pavia': [
        'Giovanni Corsico', 'Viviana Bernorio', 'Massimo Casella',
        'Alessandro Belli', 'Giovanni Susino', 'Chantall Passarella',
        'Andrea Ferraris', 'Catia Saronni', 'Daniele Longhi'
    ],
    'Romano': [
        'Anna Maria Bergamini', 'Roberta Oggionni', 'Paola Vezzoli',
        'Serena Pezzotta'
    ],
    'Varese': [
        'Alessandro Bertoni', 'Diana Accili', 'Chiara Roncari', 
        'Sara Campiglio', 'Domenico Battista', 'Donatella Gelmi',
        'Federica Platini'
    ],
    'Vigevano': [ 'Margherita Previde', 'Viola Donato' ],
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
    
    for d in folders:
        folder = '%s_Report Teams' % d.strftime("%Y-%m-%d")

        if file_date <= d:
            if reportfad:
                newpath = path.join(base, centro, 'Report FAD', folder)
            else:
                newpath = path.join(base, centro, folder)

            if not path.exists(newpath):
                makedirs(newpath)
            
            newpath = path.join(newpath, path.basename(f))
            if f not in newpath:
                #print (f'mv {f} {newpath}')
                shutil.move(f, newpath)
                file_moved = file_moved + 1

            break

print(f'Total files {total_files}')
print(f'Files moved {file_moved}')

print("Script finito.")
