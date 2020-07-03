from os import path, makedirs, chdir
import csv

base = '/Users/andrea/Fondazione Enaip Lombardia/Istruzione e Formazione Professionale - Anno Scolastico 2019 2020/Esami'
folder = '{0}/{1}_{2}-{3}-{4}'
subfolder_1 = '{0}/Documentazione Commissione'
subfolder_2 = '{0}/Raccolta tesine e output allievi'

folder_2 = '{0}/00_Verbali Commissioni Esami'
subfonder2_1 = '{0}/Terzi Anni'
subfonder2_2 = '{0}/Quarti Anni'

filename = "commissioni.csv"

with open(filename) as csv_file:
    chdir(base)

    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        #Comune;commissione esame;Id Corso;Id Sezione;Qualifica
        centro = row[0]
        if centro == "Comune": continue
        commissione = row[1] if row[1] != '' else 'XXXX'
        idcorso = row[2]
        idsez = row[3]
        qualifica = row[4]

        basepath = folder.format(centro, commissione, idcorso, idsez, qualifica)
        if not path.exists(basepath):
            print("%s" % basepath)
            makedirs(basepath)

        newpath = subfolder_1.format(basepath)
        if not path.exists(newpath):
            makedirs(newpath)

        newpath = subfolder_2.format(basepath)
        if not path.exists(newpath):
            makedirs(newpath)

        basepath = folder_2.format(centro)
        if not path.exists(basepath):
            makedirs(basepath)

        newpath = subfonder2_1.format(basepath)
        if not path.exists(newpath):
            makedirs(newpath)

        newpath = subfonder2_2.format(basepath)
        if not path.exists(newpath):
            makedirs(newpath)

    csv_file.close()

print("Script finito.")