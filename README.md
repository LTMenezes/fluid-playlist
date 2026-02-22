# Fluid Playlist

[![PyPI version](https://badge.fury.io/py/fluidPlaylists.svg)](https://badge.fury.io/py/fluidplaylist)

Fluid Playlist is a library to build fluid playlists in Spotify — playlists that gradually change music rhythm and energy without abrupt transitions. Playlists can be built using the user's saved songs and featured tracks from around the world.

Check out the [demo](https://fluid-playlists.herokuapp.com/).

![Fluid](docs/fluid-screen.png)

## Installation

```bash
pip install fluidplaylist
```

We recommend using a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

## Getting Started

Building a simple fluid playlist:

```python
from fluidplaylist import fluid

fluid_p = fluid.FluidPlaylist(
    'YOUR_CLIENT_ID',
    'YOUR_CLIENT_SECRET',
    0.1,
    "Your Fluid Playlist",
    "http://localhost:8000"
)

fluid_p.set_spotify_access_token_through_terminal()
fluid_p.build_fluid_playlist()
```

## Contributing

Feel free to open a Pull Request — I will review it as soon as possible.

## Issue Tracker

Please report bugs and enhancement ideas at:

https://github.com/LTMenezes/fluid-playlist/issues

Questions are welcome on the tracker too.

## Authors

- Leonardo Teixeira Menezes
