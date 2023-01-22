# importing required libraries
import requests, json, os

# enter your api key here
api_key = os.environ['MAPS_APIKEY']

# address to search
source = 'Via Bernardino Luini, 5, Milano'

destinations = [
    'Via S. Bernardino, 139/V Bergamo',
    'Viale Stelvio, 143 Busto Arsizio',
    'Via XI Febbraio, 8 Cantù',
    'Via Dante, 127 Como',
    'Piazzale Luzzara, 1 Cremona',
    'Via F.lli Chiesa, 3 Dalmine',
    'Via Caduti Lecchesi a Fossoli, 29 Lecco',
    'Via Novara, 10/A Magenta',
    'Via Bellonci, 1 Mantova',
    'Via S. Rocco, 3 Melzo',
    'Via Montegrappa, 21 Monticello',
    'Via Credaro, 24 Morbegno',
    'Viale Battisti, 104 Pavia',
    'Via S. Giorgio, 12 Romano di Lombardia',
    'Via Uberti, 44 Varese',
    'Corso Milano, 4 Vigevano',
    'Via Dozio, 5/7 Vimercate',
    'Via San Lorenzo, 14 Voghera',
    'Viale Trento, Lomazzo',
    'Malpensa Fiere, Via XI Settembre, Busto Arsizio'
]

# Take source as input
#source = input()

# Take destination as input
#dest = input()

# url variable store url
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'

# Get method of requests module
# return response object
for dest in destinations:
    print('Calcolo la distanza tra: ')
    print(f' - {source}')
    print(f' - {dest}')
    r = requests.get(f'{url}origins={source}&destinations={dest}&key={api_key}')

    # json method of response object
    # return json format result
    x = r.json()

    # by default driving mode considered

    # print the value of x
    distance = x['rows'][0]['elements'][0]['distance']['value']
    print(f'Distanza in metri {distance}')