import json
import os
import sharepy

if __name__ == '__main__':
    root_url = "https://enaiplombardia.sharepoint.com"
    site = 'ClassediProva'

    username = os.getenv('USERNAME', None)
    password = os.getenv('PASSWORD', None)

    s = sharepy.connect(root_url, username, password)

    collection = 'Documenti condivisi'
    filename = 'Cartella di Prova'
    groupname = 'Gruppi Amministrativi'
    role = 'Modifica'

    url = f'{root_url}/sites/{site}/_api/web/GetFolderByServerRelativeUrl(\'{collection}/{filename}\')/ListItemAllFields/breakroleinheritance(copyRoleAssignments=true, clearSubscopes=true)'
    response = s.post(url, headers={"Accept": "application/json"})
    r = json.loads(response.content)
    if 'error' in r:
        print("%s" % r)
        exit(1)
    else:
        print("Broken role inherintance.")


    url = f'{root_url}/sites/{site}/_api/web/GetFolderByServerRelativeUrl(\'{collection}/{filename}\')/ListItemAllFields/roleassignments/addroleassignment(principalid={groupname},roledefid={role})'
    response = s.post(url, headers={"Accept": "application/json"})
    r = json.loads(response.content)
    if 'error' in r:
        print("%s" % r)
        exit(1)
    else:
        print("Added role assignment.")

    print("Script finito.")