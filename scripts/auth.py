"""Module for parsing authorization details."""

import base64
import requests
import secrets
import urllib
import webbrowser


def _parse_secret_file(secret_file):
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
    raise Exception("Could not parse secret file.")


def _generate_state(nbytes=32):
    """Generates a state string for OAuth."""
    return secrets.token_urlsafe(nbytes)


def _get_auth_code(client_id, redirect_uri='https://localhost:8082'):
    """Requests an authorization code from spotify."""
    endpoint = 'https://accounts.spotify.com/authorize'
    state = generate_state()
    params = {'client_id': client_id,
              'response_type': 'code',
              'redirect_uri': redirect_uri,
              'state': state}
    # build url with endpoint and params
    url = requests.Request('GET', endpoint, params=params).prepare().url
    webbrowser.open(url)
    auth_code_url = input("Paste the auth code url here: ")
    reponse_params = _parse_auth_code_url(auth_code_url)
    if 'state' in response_params:
        assert response_params['state'] == state
    return response_params['code']


def _parse_auth_code_url(auth_code_url):
    """TODO
    example input: https://example.com/?code=CODE
    """
    url_query = urllib.parse.urlparse(auth_code_url).query
    return dict(p.split('=') for p in url_query.split('&'))


def _encode_access_key(client_id, client_secret):
    utf_secret = f"{client_id}:{client_secret}".encode('UTF-8')
    return base64.standard_b64encode(utf_secret).decode('ascii')


def _get_access_token(auth_code, client_id, client_secret):
    """Exchange authorization code with access token."""
    endpoint = 'https://accounts.spotify.com/api/token'
    params = {'grant_type': 'authorization_code',
              'code': auth_code,
              'redirect_uri': 'https://localhost:8082'}
    header = {'Authorization': _encode_access_key(client_id, client_secret)}
    #TODO
    return None


def authorize(secret_file):
    client_id, client_secret = _parse_secret_file(secret_file)
    auth_code = _get_auth_code(client_id)
    access_token = _get_access_token(auth_code, client_id, client_secret)
