import json
import os
import csv
import base64

from django.shortcuts import render
from dateutil import tz

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

from batch.download_helper import get_berarertoken, download_call_data, download_generatedexcel
from batch.auth_helper import scopes, get_sign_in_url, get_token_from_code, store_token, store_bearertoken, store_user, remove_user_and_token, get_token
from batch.graph_helper import get_meuser, get_all_groups

# Create your views here.

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Europe/Rome')

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
    request.session['ente'] = id

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

    return HttpResponseRedirect(reverse('batch_home'))

def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('batch_home'))

def home(request):
    context = initialize_context(request)
    context['appdata'] = {
        'appid': request.session.get('appid', None),
        'ente': request.session.get('ente', None),
        'scopes': scopes
    }

    return render(request, 'batch/home.html', context)

def bearer(request):
    message = "Effettuata la chiamata in modo errato."

    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            if 'token' in data and data['token']:
                store_bearertoken(request, data['token'])

            token = get_token(request)
            groups = get_all_groups(token)

            data = [{ 'name': g['displayName'], 'id': g['id'] } for g in groups]
            data = sorted(data, key=lambda k: k['name'])

            return JsonResponse({
                "esito": True,
                "message": "Registrato bearer, ecco la lista dei gruppi.",
                "data": data
            })
    except Exception as e:
        message = "%s" % e
        print("Error: %s" % message)
        
    return JsonResponse({
        "esito": False,
        "message": message
    }, status=500)

def upload_csvfile(request):
    if request.method == 'POST':
        try:
            call_ids = []

            fileContent = request.FILES.get("uploadcsv").read().decode("utf-8")
            lines = fileContent.splitlines()
            reader = csv.reader(lines, delimiter=',')
            for row in reader:
                if 'Conference' not in row[0]:
                    call_ids.append(row[0])

            return JsonResponse({
                "esito": True,
                "message": call_ids,
            })
        except Exception as e:
            return JsonResponse({
                "esito": False,
                "message": "Exception: " + str(e)
            })
        
    return JsonResponse({
        "esito": False,
        "message": "Must be invoked with POST.",
    }, status=500)


def download_jsonapi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            tries = 0
            jsonFile = None
            while jsonFile is None and tries < 2:
                if not 'token' in request.session:
                    ente = request.session['ente']
                    t = get_berarertoken(ente)
                    request.session['token'] = t

                jsonFile = download_call_data(request.session['token'], data['callId']) 
                tries += 1

                if jsonFile is None:
                    del request.session['token']

            return JsonResponse({
                "esito": True,
                "calldata": jsonFile
            })
        except Exception as e:
            return JsonResponse({
                "esito": False,
                "message": "Exception: " + str(e)
            })

    return JsonResponse({
        "esito": False,
        "message": "Must be invoked with POST.",
    }, status=500)


def generate_excel(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dictFile = json.loads(data['jsonFile'])
            reportId = data['reportId']

            tries = 0
            excelFile = None
            while excelFile is None and tries < 2:
                if not 'token' in request.session:
                    ente = request.session['ente']
                    t = get_berarertoken(ente)
                    request.session['token'] = t

                filename, excelFile = download_generatedexcel(request.session['token'], dictFile, reportId)
                tries += 1

                if excelFile is None:
                    del request.session['token']

                return JsonResponse({
                    "esito": True,
                    "filename": filename,
                    "calldata": base64.b64encode(excelFile).decode('utf-8') if excelFile is not None else None
                })
        except Exception as e:
            return JsonResponse({
                "esito": False,
                "message": "Exception: " + str(e)
            })

    return JsonResponse({
        "esito": False,
        "message": "Must be invoked with POST.",
    }, status=500)