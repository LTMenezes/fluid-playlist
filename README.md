Fluid Playlists
===================

[![PyPI version](https://badge.fury.io/py/fluidPlaylists.svg)](https://badge.fury.io/py/fluidPlaylists)

Fluid Playlists is a library to build fluid playlists in Spotify, a playlist that changes gradually the musics rhythm and energy. The goal is to provide the user with a playlist that is built without abrupt changes. Playlists can be built using the user saved songs and featured tracks from around the world.

![Fluid](docs/fluid-screen.png)

Installing Fluid Playlists
===================

You can install Fluid Playlists with:

```bash
pip install fluidPlaylists
```

We recommend using a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).


Getting Started
===================
Building a simple fluid playlist should be as simple as:
```py
from fluidPlaylists import fluid

fluid_p = fluid.FluidPlaylist('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', 0.1, "Your Fluid Playlist", "http://localhost:8000")

fluid_p.set_spotify_access_token_through_terminal()

fluid_p.build_fluid_playlist() 
```

Contributing
===================
If you'd like to contribute feel free to open a Pull Request and I will review it as soon as possible.

Issue tracker
===================
Please report any bugs and enhancement ideas in the issue tracker:

  https://github.com/LTMenezes/fluid-playlists/issues

Feel free to also ask questions on the tracker.

Authors
===================
- Leonardo Teixeira Menezes