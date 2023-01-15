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


# Leggi dati dalla query
dati = readSqlData('query.sql')
dati.to_excel("/Users/andrea/Downloads/output.xlsx", sheet_name='data')