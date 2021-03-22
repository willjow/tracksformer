"""Module for searching spotify for tracks."""

import auth

import requests


class Searcher():
    """Class to handle searching for tracks."""

    def track_search(artist, title, filters=None):
        """Searches spotify for a track.

        Parameters
        ----------
        artist : str
            The track artist.
        title : str
            The track title.
        filters : str
            TODO
        """
        endpoint = 'https://api.spotify.com/v1/search'
        params={'q': f'artist:{artist}+track:{title}',
                'type': 'track'},
        headers={'Accept': 'application/json',
                 'Content-Type': 'application/json',
                 'Authorization': #TODO}
        response = requests.get(endpoint, params, headers=headers)
