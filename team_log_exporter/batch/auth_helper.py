import yaml
import time
import os
from requests_oauthlib import OAuth2Session

# This is necessary for testing with non-HTTPS localhost
# Remove this if deploying to production
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This is necessary because Azure does not guarantee
# to return scopes in the same case and order as requested
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_IGNORE_SCOPE_CHANGE'] = '1'

# Load the oauth_settings.yml file
stream = open('oauth_settings.yml', 'r')
settings = yaml.load(stream, yaml.SafeLoader)
authorize_url = '{0}{1}'.format(settings['authority'], settings['authorize_endpoint'])
token_url = '{0}{1}'.format(settings['authority'], settings['token_endpoint'])

scopes = settings['scopes']

# Method to generate a sign-in url
def get_sign_in_url(request):
    # Initialize the OAuth client
    aad_auth = OAuth2Session(request.session.get('appid', None),
        scope = settings['scopes'],
        redirect_uri = "%s/batch/callback" % os.environ['REDIRECT_BASEURI'])

    sign_in_url, state = aad_auth.authorization_url(authorize_url, prompt='login')

    return sign_in_url, state

# Method to exchange auth code for access token
def get_token_from_code(request, callback_url, expected_state):
    # Initialize the OAuth client
    aad_auth = OAuth2Session(request.session.get('appid', None),
        state = expected_state,
        scope = settings['scopes'],
        redirect_uri = "%s/batch/callback" % os.environ['REDIRECT_BASEURI'])

    token = aad_auth.fetch_token(token_url,
        client_secret = request.session.get('appsecret', None),
        authorization_response = callback_url)

    return token

def store_token(request, token):
    request.session['oauth_token'] = token

def store_bearertoken(request, token):
    request.session['bearer_token'] = token

def store_user(request, user):
    request.session['user'] = {
        'is_authenticated': True,
        'name': user['displayName'],
        'id': user['id'],
        'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName']
    }

def get_user(request):
    user = request.session['user']
    return user
    
def get_token(request):
    token = request.session['oauth_token']
    if token is not None:
        # Check expiration
        now = time.time()
        # Subtract 5 minutes from expiration to account for clock skew
        expire_time = token['expires_at'] - 300
        if now >= expire_time:
            # Refresh the token
            aad_auth = OAuth2Session(request.session.get('appid', None),
                token = token,
                scope = settings['scopes'],
                redirect_uri = "%s/batch/callback" % os.environ['REDIRECT_BASEURI'])

            refresh_params = {
                'client_id': request.session.get('appid', None),
                'client_secret': request.session.get('appsecret', None),
            }
            new_token = aad_auth.refresh_token(token_url, **refresh_params)

            # Save new token
            store_token(request, new_token)

            # Return new access token
            return new_token

    # Token still valid (or null), just return it
    return token

def get_bearertoken(request):
    token = request.session['bearer_token']
    return token

def remove_user_and_token(request):
    if 'bearer_token' in request.session:
        del request.session['bearer_token']

    if 'oauth_token' in request.session:
        del request.session['oauth_token']

    if 'user' in request.session:
        del request.session['user']