"""Module for parsing authorization details."""

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
            return f"Basic {client_id}:{client_secret}"
    return None

