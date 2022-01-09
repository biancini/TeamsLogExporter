import sys
import getopt
import configparser
import requests
import re

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from os import path, makedirs, chdir
from shapely.geometry import Point

from utils import connect_perseo_db

pd.options.mode.chained_assignment = None


def apply_delta(dati):
    # IDedizione: (TipoFormativoInterno, TipoProgetto)
    list_delta = {
        28360: ('DOTI DISABILI', 'LLL - SOGGETTI DEBOLI ADULTI DISABILI'),
        28103: ('OBBLIGO FORMATIVO - DDIF', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        28016: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        28349: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        28049: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        28370: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        28375: ('AMPLIAMENTO OFFERTA FORMATIVA DDIF IN ALTERNANZA', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        28036: ('SERVIZI AL LAVORO - DOTI', 'LLL - LAVORATORI IN DIFFICOLTÀ OCCUPAZIONALE'),
        28313: ('ATTIVITÀ CULTURALI E RICREATIVE', 'LLL - FORMAZIONE CONTINUA/PERMANENTE'),
        29356: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        29325: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        30095: ('DOTI DISABILI', 'LLL - SOGGETTI DEBOLI ADULTI DISABILI'),
        30108: ('APPRENDISTATO PROFESSIONALIZZANTE', 'LLL - FORMAZIONE APPRENDISTATO'),
        29130: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        29559: ('TIROCINIO', 'LLL - FORMAZIONE APPRENDISTATO'),
        30532: ('APPRENDISTATO PROFESSIONALIZZANTE', 'LLL - FORMAZIONE APPRENDISTATO'),
        30296: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        30514: ('FORMAZIONE DETENUTI ED EX-DETENUTI', 'LLL - SOGGETTI DEBOLI ADULTI PENALE'),
        30297: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        30303: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        30312: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        30304: ('ATTIVITÀ DI RECUPERO DEBITI FORMATIVI', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        30470: ('DOTI DISABILI', 'LLL - SOGGETTI DEBOLI ADULTI DISABILI'),
        30270: ('OBBLIGO FORMATIVO - DDIF', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO'),
        30427: ('APPRENDISTATO PROFESSIONALIZZANTE', 'LLL - FORMAZIONE APPRENDISTATO'),
        30426: ('APPRENDISTATO PROFESSIONALIZZANTE', 'LLL - FORMAZIONE APPRENDISTATO')
    }

    for id_edizione, tipi in list_delta.items():
        if id_edizione in dati.index.tolist():
            dati.loc[id_edizione, 'TipoFormativoInterno'] = tipi[0]
            dati.loc[id_edizione, 'TipoProgetto'] = tipi[1]


def map_area(row):
    mapping_area = {
        'Formazione Giovani': ['IeFP - Primi anni', 'IeFP - Secondi anni', 'IeFP - Terzi anni', 'IeFP - Quarti anni', 'IeFP - Apprendistato', 'Integrazione Sistema Scolastico', 'IeFP - Minori disabili', 'IeFP - Penale minorile', 'IeFP - Successo formativo'],
        'Formazione Adulti Disoccupati': ['Formazione Permanente', 'Accompagnamento al lavoro', 'Orientamento', 'Tirocini extra-curricolari', 'Dote Formazione Lavoro', 'Qualifica adulti'],
        'Formazione Adulti Occupati': ['Formazione Continua', 'Formazione Abilitante', 'Apprendistato art.44 e art.45'],
        'Svantaggio': ['Disabili', 'Detenuti ed ex-detenuti', 'Stranieri'],
        'Altro e Varie': ['ITS e IFTS', 'Alta Formazione', 'Progetti Europei', 'Attività culturali e ricreative', 'Formazione personale interno']
    }
    
    for name, rules in mapping_area.items():
        attivita = 'Undefined'
        if row['attivita'] in rules:
            return name
        
    return 'Undefined'


def map_attivita(row):
    mapping_attivita = {
        # Formazione Giovani
        'IeFP - Primi anni': [('add', 'TipoProgetto', 'IFP - DDIF1')],
        'IeFP - Secondi anni': [('add', 'TipoProgetto', 'IFP - DDIF2')],
        'IeFP - Terzi anni': [('add', 'TipoProgetto', 'IFP - DDIF3')],
        'IeFP - Quarti anni': [('add', 'TipoProgetto', 'IFP - DDIF4')],
        'IeFP - Apprendistato': [('add', 'TipoProgetto', 'IFP - FORMAZIONE APPRENDISTATO')],
        'Integrazione Sistema Scolastico': [('add', 'TipoProgetto', 'IFP - INTEGRAZIONE SISTEMA SCOLASTICO')],
        'IeFP - Minori disabili': [('add', 'TipoProgetto', 'IFP - SOGGETTI DEBOLI MINORI DISABILI')],
        'IeFP - Penale minorile': [('add', 'TipoProgetto', 'IFP - SOGGETTI DEBOLI MINORI/PENALE')],
        'IeFP - Successo formativo': [('add', 'TipoProgetto', 'IFP - SUCCESSO FORMATIVO')],

        # Formazione Adulti Disoccupati
        'Formazione Permanente': [('add', 'TipoFormativoInterno', '.*PERMANENTE'), ('del', 'TipoProgetto', 'LLL - FORMAZIONE ABILITANTE'), ('del', 'TipoProgetto', 'LLL - ALTA FORMAZIONE')],
        'Accompagnamento al lavoro': [('add', 'TipoFormativoInterno', 'ACCOMPAGNAMENTO AL LAVORO'), ('del', 'TipoProgetto', 'LLL.*DEBOLI.*')],
        'Orientamento': [('add', 'TipoFormativoInterno', 'ORIENTAMENTO'), ('del', 'TipoProgetto', 'IFP.*')],
        'Tirocini extra-curricolari': [('add', 'TipoProgetto', 'SAL - TIROCINI EXTRACURRICULARI')],
        'Dote Formazione Lavoro': [('add', 'TipoFormativoInterno', 'DOTE FORMAZIONE-LAVORO')],
        'Qualifica adulti': [('add', 'TipoFormativoInterno', 'QUALIFICA ADULTI')],

        # Formazione Adulti Occupati
        'Formazione Continua': [('add', 'TipoFormativoInterno', 'FORMAZIONE CONTINUA.*'), ('add', 'TipoProgetto', 'AS - CONSULENZA.*'), ('del', 'TipoFormativoInterno', '.*PERMANENTE')],
        'Formazione Abilitante': [('add', 'TipoProgetto', '.*FORMAZIONE ABILITANTE.*')],
        'Apprendistato art.44 e art.45': [('add', 'TipoProgetto', 'LLL - FORMAZIONE APPRENDISTATO')],

        # Svantaggio
        'Disabili': [('add', 'TipoProgetto', '.*SOGGETTI DEBOLI ADULTI.*DISABILI')],
        'Detenuti ed ex-detenuti': [('add', 'TipoProgetto', 'LLL - SOGGETTI DEBOLI ADULTI PENALE')],
        'Stranieri': [('add', 'TipoProgetto', 'LLL - SOGGETTI DEBOLI ADULTI STRANIERI')],

        # Altro e Varie
        'ITS e IFTS': [('add', 'TipoProgetto', 'FS - ISTRUZIONE TECNICA SUPERIORE')],
        'Alta Formazione': [('add', 'TipoProgetto', 'FS - ALTA FORMAZIONE')],
        'Progetti Europei': [('add', 'TipoProgetto', 'LLL - PROGETTI EUROPEI')],
        'Attività culturali e ricreative': [('add', 'TipoFormativoInterno', 'ATTIVITÀ CULTURALI E RICREATIVE')],
        'Formazione personale interno': [('add', 'TipoFormativoInterno', 'FORMAZIONE PERSONALE INTERNO')]
    }

    for name, rules in mapping_attivita.items():
        attivita = 'Undefined'
        
        for (operation, field, value) in rules:
            if operation == 'add':
                if re.match(value, row[field]):
                    attivita = name
            if operation == 'del':
                if re.match(value, row[field]):
                    attivita = 'Undefined'
        
        if attivita != 'Undefined':
            return attivita
    
    return 'Undefined'


def download_materiali(engine):
    sql_file = '../PerseoDB/Costi/Ordini Materiali e Servizi.sql'
    fd = open(sql_file, 'r')
    sqlFile = fd.read()
    fd.close()

    dati = pd.read_sql(sqlFile, engine)
    
    formats = { 'U': 'currency', 'V': 'currency' }
    return dati, formats
    
    
def download_parcelle(engine):
    sql_file = '../PerseoDB/Costi/Parcelle collaboratori.sql'
    fd = open(sql_file, 'r')
    sqlFile = fd.read()
    fd.close()

    dati = pd.read_sql(sqlFile, engine)
    
    formats = { 'R': 'currency', 'S': 'currency', 'T': 'currency', 'U': 'currency', 'V': 'currency', 'W': 'currency' }
    return dati, formats


def download_fatture(engine):
    sql_file = '../PerseoDB/Costi/Fatture collaboratori.sql'
    fd = open(sql_file, 'r')
    sqlFile = fd.read()
    fd.close()

    dati = pd.read_sql(sqlFile, engine)
    dati = dati.set_index(['IDedizione'])

    apply_delta(dati)
    dati['attivita'] = dati.apply(lambda row: map_attivita(row), axis=1)
    dati['area'] = dati.apply(lambda row: map_area(row), axis=1)
    dati.reset_index(inplace=True)

    formats = { 'R': 'number', 'S': 'number', 'T': 'currency', 'U': 'currency', 'V': 'currency', 'W': 'currency', 'X': 'currency', 'Y': 'currency', 'Z': 'currency', 'AA': 'currency', 'AB': 'currency' }
    return dati, formats


def download_lista_attivita(engine):
    sql_file = '../PerseoDB/Attività/Elenco Servizi.sql'
    fd = open(sql_file, 'r')
    sqlFile = fd.read()
    fd.close()

    dati = pd.read_sql(sqlFile, engine)
    dati = dati.set_index(['IDedizione'])

    for col in ['Durata', 'OreAula', 'OreStage', 'NIscr', 'ImportoDoti']:
        dati[col] = dati[col].fillna(0)

    apply_delta(dati)
    dati['attivita'] = dati.apply(lambda row: map_attivita(row), axis=1)
    dati['area'] = dati.apply(lambda row: map_area(row), axis=1)
    dati.reset_index(inplace=True)

    formats = { 'Q': 'number', 'R': 'number', 'S': 'number', 'U': 'currency' }
    return dati, formats



def download_findata(configuration):
    engine = connect_perseo_db()
    dati = {
        'attivita': download_lista_attivita(engine),
        'fatture': download_fatture(engine),
        'parcelle': download_parcelle(engine),
        'materiali': download_materiali(engine)
    }
    
    writer = pd.ExcelWriter(configuration['filename'], engine='xlsxwriter', datetime_format='DD/MM/YYYY')
    for sheet, (df, f) in dati.items():
        df.to_excel(writer, sheet_name=sheet, startrow=1, header=False, index=False)
        worksheet = writer.sheets[sheet]
        (max_row, max_col) = df.shape
        column_settings = [{'header': column} for column in df.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

        workbook  = writer.book
        formats = {
            'number': workbook.add_format({'num_format': '#,##0'}),
            'currency': workbook.add_format({'num_format': '€ #,##0.00'})
        }

        for c, f in f.items():
            worksheet.set_column(f'{c}:{c}', None, formats[f])

    writer.save()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini', encoding='utf-8')
    ente = 'ENAIP'
    filename = '/Users/andrea/Downloads/Perseo_Findata.xlsx'

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"he:f:", ["help", "ente=", "file="])
    except getopt.GetoptError:
        print('download_findata.py')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('download_findata.py [-e <ente>] [-f <excel file>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        elif o in ('-f', '--file'):
            filename = a
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente
    configuration['filename'] = filename

    print(f'Working for institution {ente}.')
    download_findata(configuration)
    print("Script finito.")