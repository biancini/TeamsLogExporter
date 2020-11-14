import requests
import os.path
import json
from urllib import parse

def call_api(t, uri):
    head = { 'Authorization': f'Bearer {t}' }
    r = requests.get(uri, headers=head)
    response = r.json()

    return response

if __name__ == '__main__':
    tenant_id = os.getenv('TENANTID_ENAIP', None)
    client_id = os.getenv('APPID_ENAIP', None)
    client_secret =  os.getenv('APPSECRET_ENAIP', None)
    
    data = parse.urlencode({
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    })

    uri = 'https://login.microsoftonline.com/{0}/oauth2/v2.0/token'.format(tenant_id)
    r = requests.post(uri, data=data).json()

    if not 'access_token' in r:
        print(f'{r}')
        exit(1)
        
    t = r['access_token']
    #t = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCIsImtpZCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCJ9.eyJhdWQiOiJodHRwczovL2NxZC50ZWFtcy5taWNyb3NvZnQuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvYTAyMTQxZTgtMTYyMC00Yjk4LThiNDYtYTk5ZGU3ZDJiYTU3LyIsImlhdCI6MTYwNTM0MTUxMCwibmJmIjoxNjA1MzQxNTEwLCJleHAiOjE2MDUzNDU0MTAsImFjciI6IjEiLCJhaW8iOiJFMlJnWUJCU2xIb3N1RDB0OHJETkY0N0FlYk92VlVyd1Z0WXovT0FSZXRNa05xK3h3QXNBIiwiYW1yIjpbInB3ZCJdLCJhcHBpZCI6ImM2MWQ2N2NmLTI5NWEtNDYyYy05NzJmLTMzYWYzNzAwODc1MSIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiQmlhbmNpbmkiLCJnaXZlbl9uYW1lIjoiQW5kcmVhIiwiaXBhZGRyIjoiMTMwLjI1Ljg1Ljg2IiwibmFtZSI6IkFuZHJlYSBCaWFuY2luaSIsIm9pZCI6IjViOGUzZmIzLWVmZWQtNDNkMi1hMjNlLTBmNjY4Y2Q5Yzk3NSIsInB1aWQiOiIxMDAzMjAwMDlGMzE5RkNGIiwicmgiOiIwLkFTOEE2RUVob0NBV21FdUxScW1kNTlLNlY4OW5IY1phS1N4R2x5OHpyemNBaDFFdkFPay4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzdWIiOiJrVnd2aWtIb2owd3VyWEdrWWZva3lmNFhRRFhSQi13Unpmc0lGYmhSc21vIiwidGVuYW50X2N0cnkiOiJJVCIsInRpZCI6ImEwMjE0MWU4LTE2MjAtNGI5OC04YjQ2LWE5OWRlN2QyYmE1NyIsInVuaXF1ZV9uYW1lIjoiYW5kcmVhLmJpYW5jaW5pQGVuYWlwbG9tYmFyZGlhLml0IiwidXBuIjoiYW5kcmVhLmJpYW5jaW5pQGVuYWlwbG9tYmFyZGlhLml0IiwidXRpIjoiWEU0YUxlLW9Oa3FMNW5EUTluY09BQSIsInZlciI6IjEuMCJ9.wnfxgc3Q_N2LjhYZfagOmVWJTxushrZOOffsrqDdMpBwSLB4b9-xRR6N8lD9kNnoeC2HvuERZAScSv9-vagdO9OVraDiN11ebRgJybI6twuv5G0qt_zZRR8vqifwkzB3om7HSCf-GiiewK_1PHyjN4ke1CpOiiFnqjLhzLz1NJaYAvAeXZT6PAGPbRoPRs8fZO2gCsGuvQ8cPz4nXdZoVHS6fg2Pfm77zXWHsntx2rTNQZJ8G0_4_Vh3BsdUnjkKPOQ5InpBMnK81qXcH56m35OCMkfKG2UN3g8F5rkRLEZM4e5aiRiLtcCI80ZtkvGqHWoAFhH-MLjonAuyxK3hvg'

    print("%s" % t)

    #user_id = '5b8e3fb3-efed-43d2-a23e-0f668cd9c975'
    call_id =  '19:8c87ed3fe140463793daffac2c6adc8e@thread.tacv2'
    #uri = f'https://graph.microsoft.com/beta/communications/callRecords/{call_id}?$expand=sessions($expand=segments)'
    uri = f'https://cqd.teams.microsoft.com/data/emea/RunQuery'

    head = {
        'authorization': f'Bearer {t}',
        'content-type': 'application/json;charset=UTF-8',
    }

    body = {
        'Filters': [{
            'DataModelName': '[AllStreams].[Date]',
            'Caption': '2020-11-09 | 2020-11-10 | 2020-11-12 | 2020-11-11 | 2020-11-13 | 2020-11-14',
            'Value': '[2020-11-09],[2020-11-10],[2020-11-12],[2020-11-11],[2020-11-13],[2020-11-14]',
        }],
        'Dimensions': [{ 'DataModelName': '[AllStreams].[Meeting Id]' }],
        'Measurements':[{ 'DataModelName': '[Measures].[Avg Call Duration]' }],
    }

    params = {
        'mode': 'cors',
        'referrer': 'https://cqd.teams.microsoft.com/cqd/'
    }

    r = requests.post(uri, headers=head, data=json.dumps(body), params=params)
    response = r.json()

    print (f'{response}')

    print(f'Script finito.')