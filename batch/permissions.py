import json
import os
import sharepy


class Sharepoint():
    root_url = None
    site = None
    s = None

    def __init__(self, root_url, site, username, password):
        self.root_url = root_url
        self.site = site

        self.s = sharepy.connect(root_url, username, password)
        print("Connected to Sharepoint.")

    def makeCall(self, url, method='POST'):
        call_url = f'{self.root_url}/sites/{self.site}/_api/web/{url}'

        if method == 'POST':
            response = self.s.post(call_url, headers={"Accept": "application/json"})
        elif method == 'DELETE':
            response = self.s.delete(call_url, headers={"Accept": "application/json"})
        else:
            response = self.s.get(call_url, headers={"Accept": "application/json"})

        if not response.content or len(response.content) == 0:
            return None

        r = json.loads(response.content)
        
        if 'error' in r:
            print(f'Error during call %s.' % r['error'])
            return None

        if 'odata.error' in r:
            print(f'Error during call %s.' % r['odata.error'])
            return None
        
        return r

    def getGroupIdFromName(self, name):
        #r = self.makeCall(f'sitegroups/getbyname(\'{name}\')?$select=Id')
        r = self.makeCall(f'sitegroups?$select=Id,Title')
        print("%s"%r)
        if r is None: return None
        return r['Id']

    def getRoleIdFromName(self, name):
        r = self.makeCall(f'roledefinitions/getbyname(\'{name}\')?$select=Id')
        if r is None: return None
        return r['Id']

    def assignPermissions(self, collection, filename, groupname, role='Lettura'):
        groupid = self.getGroupIdFromName(groupname)
        groupid = '26'
        roleid = self.getRoleIdFromName(role)

        self.makeCall(f'GetFolderByServerRelativeUrl(\'{collection}/{filename}\')/ListItemAllFields/breakroleinheritance(copyRoleAssignments=true, clearSubscopes=true)')
        print("Broken role inherintance.")

        self.makeCall(f'GetFolderByServerRelativeUrl(\'{collection}/{filename}\')/ListItemAllFields/roleassignments/getbyprincipalid(principalid={groupid})', method='DELETE')
        self.makeCall(f'GetFolderByServerRelativeUrl(\'{collection}/{filename}\')/ListItemAllFields/roleassignments/addroleassignment(principalid={groupid},roledefid={roleid})')
        print("Added role assignment.")


if __name__ == '__main__':
    username = os.getenv('USER_NAME', None)
    password = os.getenv('PASSWORD', None)

    root_url = "https://enaiplombardia.sharepoint.com"
    site = 'ClassediProva'
    
    sObj = Sharepoint(root_url, site, username, password)
    
    collection = 'Documenti condivisi'
    filename = 'Cartella di Prova'
    groupname = 'Gruppi Amministrativi'
    role = 'Lettura'

    sObj.assignPermissions(collection, filename, groupname, role)


    print("Script finito.")