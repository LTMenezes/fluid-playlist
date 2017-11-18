import random
import bcolors as colors
from spotipy import oauth2, client

class Spotify(object):
    """
    Spotify serves as a helper to extend the spotipy library.

    Args:
        client_id (str): Spotify client id.
        client_secret (str): Spotify client secret.
        callback_url (str): Spotify callback url.
    """
    def __init__(self, client_id, client_secret, callback_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url

    def get_user_id(self, token):
        """
        Get user id.

        Args:
        token (str): Spotify access token.

        Returns:
        string: User id.
        """
        sp = client.Spotify(token)
        user = sp.me()
        return user['id']

    def welcome_user(self, token):
        """
        Welcome user in the terminal using their spotify user id.

        Args:
        token (str): Spotify access token.
        """
        sp = client.Spotify(token)
        user = sp.me()
        print(colors.BITALIC + 'Nice to meet you '+ user['id']
              + ', let\'s create your fluent playlist.' + colors.ENDC)

    def get_spotify_access_token(self):
        """
        Prompts the user in the terminal for their access token.

        Returns:
        string: User access token.
        """
        print(colors.BLUE + "Getting user token" + colors.ENDC)
        sp_credentials = oauth2.SpotifyOAuth(self.client_id, self.client_secret, self.callback_url, scope='user-library-read playlist-read-private playlist-modify-private')
        authorize_url = sp_credentials.get_authorize_url()

        print('Visit this url: ' + authorize_url)
        code = input('Input the spotify code: ')
        token = sp_credentials.get_access_token(code)
        print('This is your access token: ' + str(token['access_token']))
        return token['access_token']

    def get_authorize_url(self):
        """
        Returns a valid authorize url for user authentification.

        Returns:
        string: User authorize url
        """
        sp_credentials = oauth2.SpotifyOAuth(self.client_id, self.client_secret, self.callback_url, scope='user-library-read playlist-read-private playlist-modify-private')
        return sp_credentials.get_authorize_url()

    def get_current_user_saved_tracks(self, token, max_number_of_tracks):
        """
        Get user saved tracks.

        Args:
        token (str): Spotify access token.
        max_number_of_tracks (int): Maximum number of tracks to retrieve.

        Returns:
        Array: User saved tracks.
        """
        sp = client.Spotify(token)
        print(colors.BLUE + "Getting saved tracks" + colors.ENDC)
        saved_tracks = []
        offset = 0

        while len(saved_tracks) < max_number_of_tracks:
            input_tracks = sp.current_user_saved_tracks(min(max_number_of_tracks - len(saved_tracks), 50), offset)
            for track in input_tracks['items']:
                saved_tracks.append(track)
            
            if (input_tracks['next'] is None):
                break

            offset += 50

        print(colors.OK + "Sucessfully got "+ str(len(saved_tracks)) +" saved tracks" + colors.ENDC)    
        return saved_tracks

    def get_tracks_audio_features(self, token, tracks):
        """
        Get tracks audio features.

        Args:
        token (str): Spotify access token.
        tracks (arr): Array of tracks.

        Returns:
        Array: Tracks audio features.
        """
        audio_features = []
        sp = client.Spotify(token)

        print(colors.BLUE + "Getting "+ str(len(tracks)) + " tracks audio features" + colors.ENDC)
        for index in range(0, len(tracks), 100) :
            tracks_ids = []
            for internal_index in range(index, min(index + 100,  len(tracks))):
                tracks_ids.append(tracks[internal_index]['track']['id'])

            audio_feature = sp.audio_features(tracks_ids)
            for internal_index in range(0, len(audio_feature)):
                if audio_feature[internal_index] is not None:
                    audio_features.append(audio_feature[internal_index])

        print(colors.OK + "Sucessfully got "+ str(len(audio_features)) +" tracks audio features" + colors.ENDC)
        return audio_features

    def get_featured_tracks(self, token, max_number_of_tracks):
        """
        Get featured tracks.

        Args:
        token (str): Spotify access token.
        max_number_of_tracks (int): Maximum number of tracks.

        Returns:
        Array: Featured tracks.
        """
        print(colors.BLUE + "Getting featured tracks" + colors.ENDC)
        sp = client.Spotify(token)
        featured_playlists = sp.featured_playlists(limit=50)['playlists']['items']
        featured_tracks = []
        index = 0
        while index < len(featured_playlists):
            tracks = self.get_tracks_from_playlist(token, featured_playlists[index], max_number_of_tracks - len(featured_tracks))
            for track in tracks:
                featured_tracks.append(track)
            index += 1

        featured_tracks = random.sample(featured_tracks, max_number_of_tracks)
        print(colors.OK + "Sucessfully got "+ str(len(featured_tracks)) +" featured tracks" + colors.ENDC)    
        return featured_tracks

    def get_tracks_from_playlist(self, token, playlist, max_number_of_tracks):
        """
        Get tracks from a playlist.

        Args:
        token (str): Spotify access token.
        playlist (obj): Spotify playlist.

        Returns:
        Array: Playlist tracks.
        """
        sp = client.Spotify(token)
        user_id = playlist['owner']['id']
        playlist_id = playlist['id']
        saved_tracks = []
        offset = 0

        while len(saved_tracks) < max_number_of_tracks:
            input_tracks = sp.user_playlist_tracks(user_id, playlist_id, limit=min(max_number_of_tracks - len(saved_tracks), 100))
            for track in input_tracks['items']:
                saved_tracks.append(track)
            
            if (input_tracks['next'] is None):
                break

            offset += 100

        return saved_tracks

    def create_playlist(self, token, playlist, playlist_name):
        """
        Creates a spotify playlist.

        Args:
        token (str): Spotify access token.
        playlist (obj): Spotify playlist.
        playlist_name (str): Playlist name.
        """
        sp = client.Spotify(token)
        me_id = sp.me()['id'] 
        playlist_id = sp.user_playlist_create(me_id, playlist_name, False)['id']

        playlist_tracks_id = []
        for track in playlist:
            playlist_tracks_id.append(track['uri'])

        sp.user_playlist_add_tracks(me_id, playlist_id, playlist_tracks_id)
