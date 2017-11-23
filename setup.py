from distutils.core import setup
setup(
  name = 'fluidplaylist',
  packages = ['fluidplaylist'],
  version = '0.1.4',
  description = 'A library to build fluid playlists in Spotify.',
  author = 'Leonardo Menezes',
  author_email = 'leonardotmenezes@gmail.com',
  url = 'https://github.com/LTMenezes/fluid-playlist',
  download_url = 'https://github.com/LTMenezes/fluid-playlist/archive/master.zip',
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
