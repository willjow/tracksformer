"""Module for parsing authorization details."""

import requests
import secrets
import webbrowser
import base64

def parse_file(secret_file):
    """Returns access token for authorizing spotify API requests.

    Parameters
    ----------
    secret_file : str
        The file containing the authorization details. The first line should be
        the user client ID and the second line should be the client secret.
    """
    with open(secret_file) as sf:
        client_id = sf.readline()[:-1].split(':')[1]
        client_secret = sf.readline().split(':')[1]
        if client_id and client_secret:
            return client_id, client_secret
    return None


def generate_state(nbytes=32):
    """Generates a state string for OAuth."""
    return secrets.token_urlsafe(nbytes)


def get_auth_code(client_id, redirect_uri='https://localhost:8082'):
    """Requests an authorization code from spotify."""
    endpoint = 'https://accounts.spotify.com/authorize'
    params = {'client_id': client_id,
              'response_type': 'code',
              'redirect_uri': redirect_uri,
              'state': generate_state()}
    # build url with endpoint and params
    url = requests.Request('GET', endpoint, params=params).prepare().url
    #print(url.head)
    webbrowser.open(url)
    return None

def get_access_token(auth_code):
    """Exchange authorization code with access token."""
    endpoint = 'https://accounts.spotify.com/api/token'
    params = {'grant_type': 'authorization_code',
              'code': auth_code,
              'redirect_uri': 'https://localhost:8082' }
    header = {'Authorization': 'Basic ' + base64.standard_b64encode("{}:{}".format(client_id, client_secret).encode('UTF-8')).decode('ascii')}
    response = requests.post(endpoint, params=params, headers=header)
    json_response = response.json()
    return json_response['access_token']
