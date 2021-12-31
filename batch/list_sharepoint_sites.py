import sys
import getopt
import configparser
from utils import get_user_credentials
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant


def main(configuration):
    test_team_site_url = configuration['adminsharepointsite']

    cred = get_user_credentials()
    ctx = ClientContext(test_team_site_url).with_user_credentials(cred['username'], cred['password'])

    
    tenant = Tenant(ctx)
    result = tenant.get_site_properties_from_sharepoint_by_filters("", 0).execute_query()
    sites = []
    for siteProps in result:
        sites.append({
            'title': siteProps.properties['Title'],
            'url': siteProps.properties['Url'],
            'teams': siteProps.properties['IsTeamsConnected']
        })

    print("Ci sono %d siti: " % len(sites))
    print("Titolo;URL;Teams")
    [print("%s;%s;%s" % (a['title'], a['url'], a['teams'])) for a in sites]


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini', encoding='utf-8')
    ente = 'ENAIP'

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"he:lz:", ["help", "ente=", "zipfile="])
    except getopt.GetoptError:
        print('upload_excel.py [-e <ente>] [-z <zipfile>]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print('divide_excel.py [-e <ente>] [-z <zipfile>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente

    print(f'Working for institution {ente}.')
    main(configuration)
    print("Script finito.")