"""Module for parsing authorization details."""

import requests
import secrets

def parse_file(secret_file):
    """Returns access token for authorizing spotify API requests.

    Parameters
    ----------
    secret_file : str
        The file containing the authorization details. The first line should be
        the user client ID and the second line should be the client secret.
    """
    with open(secret_file) as sf:
        client_id = sf.readline()
        client_secret = sf.readline()
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
    response = requests.get(endpoint, params)
    json_response = response.json()
    assert json_response['state'] == params['state']
    return json_reponse['code']
