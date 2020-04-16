import json
import math
import xlwt
import os
import urllib.parse
import traceback
from io import StringIO
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from exporter.auth_helper import scopes, get_sign_in_url, get_token_from_code, store_token, store_bearertoken, store_user, remove_user_and_token, get_user, get_token, get_bearertoken
from exporter.graph_helper import get_meuser, get_otheruser, get_all_users, get_all_groups, get_group_users, get_user_meetings, get_meeting_records


def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error is not None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context

def sign_in(request):
    id = request.GET.get('id', None)
    request.session['appid'] = os.environ['APPID_%s' % id]
    request.session['appsecret'] = os.environ['APPSECRET_%s' % id]

    print ("appid = %s" % request.session.get('appid', None))
    print ("appsecret = %s" % request.session.get('appsecret', None))

    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url(request)
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)

def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request, request.get_full_path(), expected_state)

    # Get the user's profile
    user = get_meuser(token)

    # Save token and user
    store_token(request, token)
    store_user(request, user)

    return HttpResponseRedirect(reverse('home'))

def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))

def home(request):
    context = initialize_context(request)
    context['appdata'] = {
        'appid': request.session.get('appid', None),
        'scopes': scopes
    }

    return render(request, 'exporter/home.html', context)

@csrf_exempt
def bearer(request):
    message = "Effettuata la chiamata in modo errato."

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            if 'token' in data and data['token']:
                store_bearertoken(request, data['token'])

            token = get_token(request)
            groups = get_all_groups(token)

            return JsonResponse({
                "esito": True,
                "message": "Registrato bearer, ecco la lista dei gruppi.",
                "data": [{ 'name': g['displayName'], 'id': g['id'] } for g in groups]
            })
    except Exception as e:
        message = "%s" % e
        print("Error: %s" % message)
        
    return JsonResponse({
        "esito": False,
        "message": message
    }, status=500)

@csrf_exempt
def getusers_bygroup(request):
    message = "Effettuata la chiamata in modo errato."

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            group_ids = data['groups']

            token = get_token(request)
            
            if len(group_ids) > 0:
                users = []
                for gid in group_ids:
                    newusers = get_group_users(token, gid)
                    users.extend(newusers)
            else:
                users = get_all_users(token)

            return JsonResponse({
                "esito": True,
                "message": "Ecco la lista degli utenti.",
                "data": [{ 'name': u['displayName'], 'id': u['id'] } for u in users]
            })
    except Exception as e:
        message = "%s" % e
        print("Error: %s" % message)
        
    return JsonResponse({
        "esito": False,
        "message": message
    }, status=500)

@csrf_exempt
def getuser_meetings(request):
    message = "Effettuata la chiamata in modo errato."

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user_ids = data['users']

            token = get_bearertoken(request)

            events = []
            if len(user_ids) > 0:
                for uid in user_ids:
                    newevents = get_user_meetings(token, uid)
                    events.extend(newevents)

            return JsonResponse({
                "esito": True,
                "message": "Ecco la lista degli utenti.",
                "data": [{ 'start': e['startDateTime'], 'end': e['endDateTime'], 'partecipant': e['participantCount'], 'id': e['id'] } for e in events]
            })
    except Exception as e:
        message = "%s" % e
        print("Error: %s" % message)

    return JsonResponse({
        "esito": False,
        "message": message
    }, status=500)

@csrf_exempt
def getmeeting_records(request):
    message = "Effettuata la chiamata in modo errato."

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            event_ids = data['meetings']

            token = get_bearertoken(request)
            graph_token = get_token(request)
            uid = get_user(request)['id']
            
            meeting_records = []
            print("%s"%event_ids)
            if len(event_ids) > 0:
                for eid in event_ids:
                    result = get_meeting_records(token, uid, eid)
                    participants = []

                    for p in result:
                        uid = p['userId']
                        user = get_otheruser(graph_token, uid)
                        name = user['displayName'] if 'displayName' in user else 'Sconosciuto'

                        min_start = None
                        max_end = None
                        duration = 0

                        for c in p['communicationFragments']:
                            start = datetime.strptime(c['startDateTime'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
                            if min_start is None or start < min_start:
                                min_start = start

                            end = datetime.strptime(c['endDateTime'].split('.', 1)[0], '%Y-%m-%dT%H:%M:%S')
                            if max_end is None or end > max_end:
                                max_end = end
                            
                            duration += c['callDuration']

                        duration /= 1000
                        duration /= 60
                        hours = math.floor(duration / 60)
                        minutes = math.floor(duration % 60)
                        duration = "{0} ore e {1} minuti".format(hours, minutes)

                        participants.append({ 'uid': uid, 'name': name, 'start': min_start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'end': max_end.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'duration': duration})

                    meeting_records.append({ 'id': eid, 'participants': participants })

            return JsonResponse({
                "esito": True,
                "message": "Ecco la lista degli utenti.",
                "data": meeting_records
            })

    except Exception as e:
        message = "%s" % e
        print("Error: %s" % message)
        traceback.print_exc()
        
    return JsonResponse({
        "esito": False,
        "message": message
    }, status=500)

@csrf_exempt
def export_xls(request):
    message = "Effettuata la chiamata in modo errato."

    try:
        if request.method == 'POST':
            data = urllib.parse.unquote(request.POST.get("table", "{}"))
            table = json.loads(data)

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Partecipante', 'Inizio presenza', 'Fine presenza', 'Tempo di partecipazione']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            font_style = xlwt.XFStyle()

            for t in table['participants']:
                row = [t['name'], t['start'], t['end'], t['duration']]
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Registro.xls"'
            wb.save(response)
            return response

    except Exception as e:
        message = "%s" % e
        print("Error: %s" % message)
    
    return JsonResponse({
        "esito": False,
        "message": message
    }, status=500)