import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib import gridspec
from scipy import stats

class Plot(object):
    """
    Plot offers methods to calculate math related problems for fluid playlists and plot
    user debug graphs.
    """

    def create_user_debug_graphs_2d(self, tracks_audio_features, axis_x, axis_y, output_folder):
        """
        Create user debug graphs from tracks in a 2-dimension space.

        Args:
        tracks_audio_features (arr): Tracks with audio features.
        axis_x (str): Axis x name.
        axis_y (str): Axis y name.
        output_folder (str): Output folder for created graphs.
        """
        self.plot_tracks(tracks_audio_features, axis_x, axis_y,
                         output_folder + '/pure-data.png')
        self.plot_tracks_with_lstsq_second_degree(tracks_audio_features, axis_x, axis_y,
                                                  output_folder + '/second-degree-slope.png')
        self.plot_tracks_with_lstsq_first_degree(tracks_audio_features, axis_x,
                                                 axis_y, output_folder + '/first-degree-slope.png')

    def get_second_degree_slope_points(self, tracks_audio_features, axis_x, axis_y, number_of_points):
        """
        Get a least square second degree slope from the given tracks.

        Args:
        tracks_audio_features (arr): Tracks with audio features.
        axis_x (str): Axis x name.
        axis_y (str): Axis y name.
        number_of_points (int): Number of points to define the slope.

        Returns:
        Array: Values of time.
        Array: Values of the function in the time.
        """
        points_x = []
        points_y = []

        for track in tracks_audio_features:
            points_x.append(track[axis_x])
            points_y.append(track[axis_y])

        x = np.array(points_x)
        x_square = np.array(points_x)**2
        y = np.array(points_y)
        A = np.vstack([x_square, x, np.ones(len(x))]).T

        (coeffs, _, _, _) = np.linalg.lstsq(A, y)
        function = np.poly1d(coeffs)
        time = np.linspace(0, 1, number_of_points)
        return time, function(time)

    def plot_tracks(self, tracks_audio_features, axis_x, axis_y, output_path):
        """
        Plot tracks in a 2-dimensional graph.

        Args:
        tracks_audio_features (arr): Tracks with audio features.
        axis_x (str): Axis x name.
        axis_y (str): Axis y name.
        output_path (str): Output path for the graph.
        """
        fig, ax = plt.subplots()
        plt.axis([0, 1, 0, 1])
        points_x = []
        points_y = []

        for track in tracks_audio_features:
            points_x.append(track[axis_x])
            points_y.append(track[axis_y])

        ax.plot(points_x, points_y, 'ro', markersize=2)
        plt.xlabel(axis_x)
        plt.ylabel(axis_y)
        fig.savefig(output_path)
        plt.close(fig)

    def plot_tracks_with_lstsq_second_degree(self, tracks_audio_features, axis_x, axis_y, output_path):
        """
        Plot tracks in a 2-dimensional graph and a least squares curve to fit the tracks.

        Args:
        tracks_audio_features (arr): Tracks with audio features.
        axis_x (str): Axis x name.
        axis_y (str): Axis y name.
        output_path (str): Output path for the graph.
        """
        fig, ax = plt.subplots()
        plt.axis([0, 1, 0, 1])
        points_x = []
        points_y = []

        for track in tracks_audio_features:
            points_x.append(track[axis_x])
            points_y.append(track[axis_y])

        ax.plot(points_x, points_y, 'ro', markersize=2)

        x = np.array(points_x)
        x_square = np.array(points_x)**2
        y = np.array(points_y)
        A = np.vstack([x_square, x, np.ones(len(x))]).T

        (coeffs, _, _, _) = np.linalg.lstsq(A, y)
        function = np.poly1d(coeffs)
        time = np.linspace(0, 1, 100)
        y_est = function(time)
        plt.plot(time, y_est, 'o-', label='estimate', markersize=1)
        plt.xlabel(axis_x)
        plt.ylabel(axis_y)
        fig.savefig(output_path)
        plt.close(fig)

    def plot_tracks_with_lstsq_first_degree(self, tracks_audio_features, axis_x, axis_y, output_path):
        fig, ax = plt.subplots()
        plt.axis([0, 1, 0, 1])
        points_x = []
        points_y = []

        for track in tracks_audio_features:
            points_x.append(track[axis_x])
            points_y.append(track[axis_y])

        ax.plot(points_x, points_y, 'ro', markersize=2)

        x = np.array(points_x)
        y = np.array(points_y)
        A = np.vstack([x, np.ones(len(x))]).T

        (coeffs, _, _, _) = np.linalg.lstsq(A, y)
        function = np.poly1d(coeffs)
        time = np.linspace(0, 1, 100)
        y_est = function(time)
        plt.plot(time, y_est, 'o-', label='estimate', markersize=1)
        plt.xlabel(axis_x)
        plt.ylabel(axis_y)
        fig.savefig(output_path)
        plt.close(fig)
