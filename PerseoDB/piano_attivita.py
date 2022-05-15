from sqlalchemy import create_engine
import pandas as pd
import urllib
import pyodbc
import os

def connect_perseo_db():
    server = os.environ['PERSEO_IP']
    database = os.environ['PERSEO_DB']
    username = os.environ['PERSEO_USR']
    password = os.environ['PERSEO_PWD']
    
    params = urllib.parse.quote_plus("DRIVER={FreeTDS};"
                                     "SERVER="+server+";"
                                     "PORT=1433;"
                                     "DATABASE="+database+";"
                                     "UID="+username+";"
                                     "PWD="+password+";"
                                     "Trusted_Connection=no")
    
    conn = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    return conn

def readSqlData(file_name):
    file = open(file_name, mode='r')
    query = file.read()
    file.close()

    engine = connect_perseo_db()
    return pd.read_sql(query, engine)


# Leggi l'elenco attività
dati = readSqlData('Attività/Elenco Servizi.sql')

dati[['OreAula', 'OreStage']] = dati[['OreAula', 'OreStage']].fillna(0)
dati = dati.set_index('IDedizione')

# Aggiungi i dati sulle doti (numero e importo)
doti = readSqlData('Ricavi/Doti.sql')

doti = doti.set_index('IDedizione')

dati = dati.join(doti[['NumeroDoti', 'ImportoDoti']])
dati[['NumeroDoti', 'ImportoDoti']] = dati[['NumeroDoti', 'ImportoDoti']].fillna(0)

# Aggiungi i dati sulle fatture collaboratori
fatture = readSqlData('Costi/Fatture collaboratori.sql')

fatture['Attivita'] = fatture['TipoAttivita'].map({
    'DOCENZA': 'Docenza',
    'ELABORAZIONE MATERIALE DIDATTICO': 'Docenza',
    'FORMAZIONE IN ASSETTO LAVORATIVO EXTRA MONTE ORE': 'Docenza',
    'TUTOR': 'Tutoraggio',
    'CODOCENZA': 'Docenza',
    'SOSTEGNO': 'Tutoraggio',
    'ATTIVITÀ PREVISTA DAL PROGETTO': 'Amministrazione e segreteria',
    'SERVIZI PERSONALIZZATI': 'Tutoraggio',
    'TUTOR D\'AULA': 'Tutoraggio',
    'SOSTEGNO FUORI AULA': 'Tutoraggio',
    'ORIENTAMENTO': 'Orientamento',
    'COORDINAMENTO': 'Progettazione e coordinamento',
    'ESAME': 'Esami',
    'SOSTEGNO FINANZIATO': 'Tutoraggio',
    'PROMOZIONE INTERVENTO': 'Promozione',
    'SOSTEGNO FINANZIATO FUORI AULA': 'Tutoraggio',
    'PROGETTAZIONE E PROGRAMMAZIONE DIDATTICA': 'Progettazione e coordinamento',
    'MONITORAGGIO IN ITINERE ED EX POST': 'Amministrazione e segreteria',
    'VERIFICA/VALUTAZIONE DEGLI APPRENDIMENTI': 'Esami',
    'SERVIZI AL LAVORO': 'Amministrazione e segreteria',
    'ELABORAZIONE REPORTS E STUDI': 'Amministrazione e segreteria',
    'AMMINISTRAZIONE': 'Amministrazione e segreteria',
    'SELEZIONE': 'Amministrazione e segreteria',
    'CODOCENZA ESAME': 'Esami',
    'ATTIVITÀ DI RECUPERO': 'Docenza',
    'COACHING': 'Tutoraggio',
    'DIREZIONE': 'Amministrazione e segreteria',
    'AUSILIARIO': 'Tutoraggio',
    'RICERCA': 'Promozione',
    'SCOUTING': 'Promozione',
    'SEGRETERIA': 'Amministrazione e segreteria',
    'ANALISI DEI BISOGNI': 'Progettazione e coordinamento',
    'FORMAZIONE IN ASSETTO LAVORATIVO': 'Amministrazione e segreteria'
})

fatture = fatture[['IDedizione', 'Attivita', 'sngTotale' ]].groupby(['IDedizione', 'Attivita']).sum()
fatture.columns = ['FattureCollaboratori' if x == 'sngTotale' else x for x in fatture.columns]

dati = dati.join(fatture)
dati['FattureCollaboratori'] = dati['FattureCollaboratori'].fillna(0)

# Aggiungi i dati sulle parcelle collaboratori
parcelle = readSqlData('Costi/Parcelle collaboratori.sql')
parcelle = parcelle[parcelle['IDedizione'].notna()]

parcelle['Attivita'] = parcelle['TipoCausaleParcella'].map({
    'PRATICHE NOTARILI PER ATS': 'Amministrazione e segreteria',
    'ALTRO': 'Amministrazione e segreteria',
    'COMMISSIONE DI ESAME': 'Esami',
    'ADEMPIMENTI L.626': 'Amministrazione e segreteria',
    'CONSULENZA': 'Amministrazione e segreteria'
})

parcelle = parcelle[['IDedizione', 'Attivita', 'sngTotale' ]].groupby(['IDedizione', 'Attivita']).sum()
parcelle.columns = ['ParcelleCollaboratori' if x == 'sngTotale' else x for x in parcelle.columns]

dati = dati.join(parcelle)
dati['ParcelleCollaboratori'] = dati['ParcelleCollaboratori'].fillna(0)

# Salva i dati in excel
dati = dati.reset_index(level=['Attivita'])
dati.to_excel("/Users/andrea/Downloads/output.xlsx", sheet_name='data')