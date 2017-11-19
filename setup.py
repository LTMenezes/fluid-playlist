from distutils.core import setup
setup(
  name = 'fluidPlaylists',
  packages = ['fluidPlaylists'],
  version = '0.1.4',
  description = 'A library to build fluid playlists in Spotify.',
  author = 'Leonardo Menezes',
  author_email = 'leonardotmenezes@gmail.com',
  url = 'https://github.com/LTMenezes/fluid-playlists',
  download_url = 'https://github.com/LTMenezes/fluid-playlists/archive/master.zip',
  install_requires=[
   'bcolors',
   'matplotlib',
   'numpy',
   'scipy',
   'spotipy'
  ],
  keywords = ['fluid', 'playlist', 'spotify'],
  classifiers = [],
)
