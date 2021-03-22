"""Module for parsing authorization details."""

import base64
import requests
import secrets
import urllib
import webbrowser


class Authorizer():
    """Class for handling authentication.

    Attributes
    ----------
    redirect_uri : str
        The uri to redirect to after getting the auth code.
    client_id : str
        The client id.
    client_secret : str
        The client secret.
    base64_secret : str
        The base64 ascii encoding of the client_id and client_secret.
    access_token : str
        An access token that can be provided in subsequent calls, for example
        to Spotify Web API services.
    token_type : str
        How the access token may be used: always “Bearer”.
    scope : str
        A space-separated list of scopes which have been granted for this
        access_token
    expires_in : int
        The time period (in seconds) for which the access token is valid.
    refresh_token : str
        A token that can be sent to the Spotify Accounts service in place of an
        authorization code. (When the access code expires, send a POST request
        to the Accounts service /api/token endpoint, but use this code in place
        of an authorization code. A new access token will be returned. A new
        refresh token might be returned too.)
    """

    AUTHORIZE_ENDPOINT = 'https://accounts.spotify.com/authorize'
    TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'

    def __init__(self, secret_file, redirect_uri='https://localhost:8082'):
        self.redirect_uri = redirect_uri
        self._parse_secret_file(secret_file)
        self.base64_secret = Authorizer._encode_access_key(self.client_id,
                                                           self.client_secret)
        self._get_auth_code()
        self._exchange_access_token()

    def _encode_access_key(client_id, client_secret):
        """Returns the base64 encoding of the client_id and client_secret."""
        utf_secret = f"{client_id}:{client_secret}".encode('UTF-8')
        base64_secret = base64.standard_b64encode(utf_secret).decode('ascii')
        return f"Basic {base64_secret}"

    def _parse_secret_file(self, secret_file):
        """Reads secret file to obtain client_id and client_secret.

        Parameters
        ----------
        secret_file : str
            The file containing the authorization details. The first line
            should be the user client ID and the second line should be the
            client secret.
        """
        with open(secret_file) as sf:
            self.client_id = sf.readline().rstrip('\n')
            self.client_secret = sf.readline().rstrip('\n')

    def _generate_state(nbytes=32):
        """Generates a state string for OAuth."""
        return secrets.token_urlsafe(nbytes)

    def _parse_auth_code_url(auth_code_url):
        """TODO
        example input: https://example.com/?code=CODE
        """
        url_query = urllib.parse.urlparse(auth_code_url).query
        return dict(p.split('=') for p in url_query.split('&'))

    def _get_auth_code(self):
        """Requests an authorization code from spotify and updates the relevant
        instance attribute.
        """
        state = Authorizer._generate_state()
        params = {'client_id': self.client_id,
                  'response_type': 'code',
                  'redirect_uri': self.redirect_uri,
                  'state': state}
        # build url with endpoint and params
        url = requests.Request('GET', Authorizer.AUTHORIZE_ENDPOINT,
                               params=params).prepare().url
        webbrowser.open(url)
        auth_code_url = input("Paste the auth code url here: ")
        response_params = Authorizer._parse_auth_code_url(auth_code_url)
        if 'state' in response_params:
            assert response_params['state'] == state
        self.auth_code = response_params['code']

    def _exchange_access_token(self):
        """Exchange authorization code with access token and updates the
        relevant instance attributes.
        """
        params = {'grant_type': 'authorization_code',
                  'code': self.auth_code,
                  'redirect_uri': self.redirect_uri}
        header = {'Authorization': self.base64_secret}
        response = requests.post(Authorizer.TOKEN_ENDPOINT,
                                 data=params, headers=header)
        response_json = response.json()
        self.access_token = response_json['access_token']
        self.token_type = response_json['token_type']
        self.token_expires_in = response_json['expires_in']
        self.refresh_token = response_json['refresh_token']
        if 'scope' in response_json:
            self.token_scope = response_json['scope']
        else:
            self.token_scope = None
