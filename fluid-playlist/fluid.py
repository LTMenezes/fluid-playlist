import matplotlib
matplotlib.use('Agg')
import spotify_helper
import plot
import math
import os
import errno
import config

class FluidPlaylist():
    """
    FluidPlaylist is responsible for building spotify users a fluid playlist
    using a mix of their saved musics and musics featured from the top playlists
    from around the world.
    """

    def __init__(self, sp_client_id, sp_client_secret, details_threshold, playlist_name, callback_url):
        self.spotify_client_id = sp_client_id
        self.spotify_client_server = sp_client_secret
        self.details_threshold = details_threshold
        self.playlist_name = playlist_name
        self.spotify = spotify_helper.Spotify(
            self.spotify_client_id, self.spotify_client_server, callback_url)
        self.plot = plot.Plot()
        self.spotify_token = None

    def run_main_flow(self):
        """
        Default execution to build a fluid playlist. Builds a fluid playlist and create
        output graphs from user data.
        """
        self.set_spotify_access_token_through_terminal()
        playlist, user_tracks, featured_tracks = self.build_fluid_playlist()
        user_id = self.spotify.get_user_id(self.spotify_token)
        self.create_output_graphs(user_id, user_tracks, featured_tracks, playlist)

    def set_spotify_access_token_through_terminal(self):
        """
        Sets the class spotify access token prompting the user in the terminal.
        """
        self.spotify_token = self.spotify.get_spotify_access_token()

    def get_spotify_authorize_url(self):
        """
        Returns a valid spotify authorize url.abs

        Returns:
        String: Spotify authorize url
        """
        return self.spotify.get_authorize_url()

    def build_fluid_playlist(self):
        """
        Builds a fluid playlist.

        Returns:
        Array: Array with the created playlist tracks.
        Array: Array of user tracks with details.
        Array: Array of featured tracks with details.
        """
        self.spotify.welcome_user(self.spotify_token)
        user_tracks = self.spotify.get_current_user_saved_tracks(self.spotify_token, 2000)
        user_tracks_details = self.spotify.get_tracks_audio_features(
            self.spotify_token, user_tracks)

        featured_tracks = self.spotify.get_featured_tracks(self.spotify_token, 2000)

        featured_tracks_details = self.spotify.get_tracks_audio_features(
            self.spotify_token, featured_tracks)

        self.remove_duplicated_tracks(featured_tracks_details)

        x_list, y_list = self.plot.get_second_degree_slope_points(
            user_tracks_details, 'energy', 'danceability', 100)

        playlist = self.select_playlist_tracks(
            user_tracks_details, featured_tracks_details,
            x_list, y_list, 0.01, 'energy', 'danceability')

        self.spotify.create_playlist(self.spotify_token, playlist, self.playlist_name)

        return playlist, user_tracks_details, featured_tracks_details

    def create_output_graphs(self, user_id, user_tracks_details, featured_tracks_details, created_playlist):
        """
        Create output graphs.

        Args:
        user_id (str): Spotify user id.
        user_tracks_details (arr): List of user tracks with details.
        featured_tracks_details (arr): List of featured tracks with details.
        created_playlist (arr): Created fluid playlist array of tracks.
        """
        self.create_graphs_output_folders(user_id)

        self.plot.create_user_debug_graphs_2d(
            user_tracks_details, 'energy', 'danceability', user_id)

        self.plot.plot_tracks(
            featured_tracks_details, 'energy', 'danceability',
            user_id + '/featured-tracks-pure-data.png')

        self.plot.create_user_debug_graphs_2d(
            created_playlist, 'energy', 'danceability', user_id + '/generated')

    @staticmethod
    def create_graphs_output_folders(user_id):
        """
        Create fluid playlists default output folders from graphs.
        """
        if not os.path.exists(user_id):
            os.makedirs(user_id)
        if not os.path.exists(user_id + '/generated'):
            os.makedirs(user_id + '/generated')

    def select_playlist_tracks(self, user_tracks, input_featured_tracks, slope_x, slope_y, initial_threshold, axis_x, axis_y):
        """
        Select suitable tracks to build a fluid playlist.

        Args:
        user_tracks (arr): List of user tracks with details.
        input_featured_tracks (arr): List of featured tracks with details.
        slope_x (arr): Array of points x axis values in curve.
        slope_y (arr): Array of points y axis values in curve.
        initial_threshold (float): Initial details threshold.
        axis_x (str): Used axis y identification name.
        axis_y (str): Used axis y identification name.

        Returns:
        Array: Array with the playlist tracks.
        """
        playlist = []

        for index, _ in enumerate(slope_x):
            has_track_been_chosen = False
            threshold = initial_threshold
            while has_track_been_chosen is False:
                chosen_track = self.select_track_for_given_point(
                    user_tracks, input_featured_tracks, slope_x[index],
                    slope_y[index], threshold, axis_x, axis_y)

                if chosen_track is not None:
                    has_track_been_chosen = True
                    playlist.append(chosen_track)
                else:
                    threshold += 0.01

            track_id_in_user_tracks = self.try_get_track_index_in_array(
                chosen_track, user_tracks)
            track_id_in_featured_tracks = self.try_get_track_index_in_array(
                chosen_track, input_featured_tracks)
            if track_id_in_user_tracks is not None: 
                user_tracks.pop(track_id_in_user_tracks)
            if track_id_in_featured_tracks is not None: 
                input_featured_tracks.pop(track_id_in_featured_tracks)

        return playlist

    def select_track_for_given_point(self, user_tracks, input_featured_tracks, point_x, point_y, threshold, axis_x, axis_y):
        """
        Select a suitable track for a given point.

        Args:
        user_tracks (arr): List of user tracks with details.
        input_featured_tracks (arr): List of featured tracks with details.
        point_x (arr): Point x axis value.
        point_y (arr): Point y axis value.
        initial_threshold (float): Details threshold.
        axis_x (str): Used axis y identification name.
        axis_y (str): Used axis y identification name.

        Returns:
        Array: Array with the chosen track.
        """
        minimal_distance = 999999
        has_track_been_chosen = False
        chosen_track = None
        for _, value in enumerate(user_tracks):
            if(value[axis_x] is None) or (value[axis_y] is None):
                continue
            dist = math.hypot(point_x - value[axis_x],
                              point_y - value[axis_y])
            if (dist <= threshold) and (dist < minimal_distance):
                minimal_distance = dist
                chosen_track = value
                has_track_been_chosen = True

        if has_track_been_chosen is False:
            for _, value in enumerate(input_featured_tracks):
                if ((value[axis_x] is None)
                        or (value[axis_y] is None)):
                    continue
                dist = math.hypot(point_x - value[axis_x],
                                  point_y - value[axis_y])
                if (dist <= threshold) and (dist < minimal_distance):
                    minimal_distance = dist
                    chosen_track = value

        return chosen_track

    def remove_duplicated_tracks(self, track_list):
        """
        Remove duplicated tracks inside a track list.

        Args:
        track_list (arr): List of tracks.
        """
        indexes_to_be_removed = []
        for outer_index, track in enumerate(track_list):
            for inner_index in range(outer_index + 1, len(track_list)):
                if track['id'] == track_list[inner_index]['id']:
                    indexes_to_be_removed.append(inner_index)

        #remove duplicate indexes
        indexes_to_be_removed = list(set(indexes_to_be_removed))
        #We need to remove in reverse order to maintain order
        indexes_to_be_removed.sort(reverse=True)

        for _, index in enumerate(indexes_to_be_removed):
            track_list.pop(index)

    def try_get_track_index_in_array(self, track, track_list):
        """
        Try to get a track index inside an array

        Args:
        track(arr): Track.
        track_list (arr): List of tracks.

        Returns:
        Array: Index of the track in the array or None if it isnt in the array.
        """
        for index, it_track in enumerate(track_list):
            if it_track['id'] == track['id']:
                return index

        return None


if __name__ == "__main__":
    APP = FluidPlaylist(config.SPOTIFY['client_id'], config.SPOTIFY['client_secret'], config.FLUIDCONFIG['details_threshold'], config.FLUIDCONFIG['playlist_name'], config.FLUIDCONFIG['callback_url'])
    APP.run_main_flow()
