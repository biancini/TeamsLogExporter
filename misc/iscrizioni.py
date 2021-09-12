from io import StringIO
import csv
import re

file = open('/Users/andrea/Downloads/esportazione-iscritti-da 30 a 760.csv', mode='r')
allfile = file.read()
allfile = allfile.replace('&#039;', '\'')
file.close()

try:
    while True:
        regex = re.compile(r"\"Provincia:(.*)\nComune:(.*)\nCAP:(\d+)\"")
        matches = regex.search(allfile).groups()
        allfile = regex.sub("\"%s,%s,%s\"" % matches, allfile, 1)
except AttributeError:
    pass

try:
    while True:
        regex = re.compile(r"\"Sede Formativa:(.*)\nIscrizione all'annualità 2021-2022:(.*)\nTitolo corso scelto:(.*)\"")
        matches = regex.search(allfile).groups()
        allfile = regex.sub("\"%s,%s,%s\"" % matches, allfile, 1)
except AttributeError:
    pass

f = StringIO(allfile)
reader = csv.reader(f, delimiter=';')
for row in reader:
    if 'ID' in row[0]:
        row[75:76] = ('Provincia di Residenza', 'Comune di Residenza', 'CAP di Residenza')
        row[70:71] = ('Provincia di Nascita',   'Comune di Nascita',   'CAP di Nascita')
        row[54:55] = ('Provincia di Nascita',   'Comune di Nascita',   'CAP di Nascita')
        row[41:42] = ('Provincia di Residenza', 'Comune di Residenza', 'CAP di Residenza')
        row[29:30] = ('Sede',                   'Annualità',           'Corso')
        row[15:16] = ('Provincia di Domicilio', 'Comune di Domicilio', 'CAP di Domicilio')
        row[11:12] = ('Provincia di Residenza', 'Comune di Residenza', 'CAP di Residenza')
        row[ 9:10] = ('Provincia di Nascita',   'Comune di Nascita',   'CAP di Nascita')
    else:
        for pos in [75, 70, 54, 41, 29, 15, 11, 9]:
            vals = row[pos].split(',') if ',' in row[pos] else ['', '', '']
            row[pos:pos+1] = (vals[0], vals[1], vals[2])
    
    print(';'.join(row))