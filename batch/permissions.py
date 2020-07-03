import os
import json
import requests
from urllib import parse

from office365.runtime.auth import UserCredential
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext
from office365.runtime.http.http_method import HttpMethod

if __name__ == '__main__':
    collection = 'Documenti condivisi'
    filename = 'Cartella di Prova'
    groupname = 'Gruppi Amministrativi'
    role = 'Modifica'
    site = 'https://enaiplombardia.sharepoint.com/sites/ClassediProva'

    ctx = ClientContext.connect_with_credentials(site, UserCredential('andrea.biancini@enaiplombardia.it', 'St3f4n!a'))
    request = RequestOptions(f'{site}/_api/web/')
    response = ctx.execute_request_direct(request)
    r = json.loads(response.content)
    if 'error' in r:
        print("%s" % r)
        exit(1)
    print("Logged in.")
    
    # break role inheritance
    url = f'{site}/_api/web/GetFolderByServerRelativeUrl(\'{collection}/{filename}\')/ListItemAllFields/breakroleinheritance(copyRoleAssignments=true, clearSubscopes=true)'
    request = RequestOptions(url)
    request.method = HttpMethod.Post
    response = ctx.execute_request_direct(request)
    r = json.loads(response.content)
    if 'error' in r:
        print("%s" % r)
        exit(1)
    else:
        print("Broken role inherintance.")
    
    # add assignment
    url = f'{site}/_api/web/GetFolderByServerRelativeUrl(\'{collection}/{filename}\')/ListItemAllFields/roleassignments/addroleassignment(principalid={groupname},roledefid={role})'
    request = RequestOptions(url)
    request.method = HttpMethod.Post
    response = ctx.execute_request_direct(request)
    r = json.loads(response.content)
    if 'error' in r:
        print("%s" % r)
        exit(1)
    print("Added role assignment.")

    print("Script finito.")