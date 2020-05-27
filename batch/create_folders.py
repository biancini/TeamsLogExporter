from os import path, remove, makedirs, chdir

base = 'D:\Fondazione Enaip Lombardia\Pianificazione Attività - Documenti'
chdir(base)

folder_impiego = '{0}/Impiego Settimanale/13_Impiego persone 1-5 giu-20'
folder_timesheet_1 = '{0}/Time sheet/Collaboratori/13_Settimana 1-5 giu-20'
folder_timesheet_2 = '{0}/Time sheet/Dipendenti/13_Settimana 1-5 giu-20'

centri = [ 'Bergamo', 'Botticino', 'Busto Arsizio', 'Cantu',
    'Como', 'Cremona', 'Dalmine', 'Lecco', 'Magenta',
    'Mantova', 'Melzo', 'Milano Giacinti', 'Monticello', 'Morbegno',
    'Pavia', 'Romano', 'Varese', 'Vigevano', 'Vimercate', 'Voghera' ]

for c in centri:
    newpath = folder_impiego.format(c)
    if not path.exists(newpath):
        makedirs(newpath)

    newpath = folder_timesheet_1.format(c)
    if not path.exists(newpath):
        makedirs(newpath)

    newpath = folder_timesheet_2.format(c)
    if not path.exists(newpath):
        makedirs(newpath)

print("Script finito.")