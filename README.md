# Fluid Playlist

[![PyPI version](https://badge.fury.io/py/fluidPlaylists.svg)](https://badge.fury.io/py/fluidplaylist)

A library to build fluid Spotify playlists that gradually change in rhythm and energy, avoiding abrupt transitions. [Demo](https://fluid-playlists.herokuapp.com/)

## Install

```bash
pip install fluidplaylist
```

## Usage

```py
from fluidplaylist import fluid

fluid_p = fluid.FluidPlaylist('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', 0.1, "Your Fluid Playlist", "http://localhost:8000")
fluid_p.set_spotify_access_token_through_terminal()
fluid_p.build_fluid_playlist()
```

## Contributing

Open a Pull Request or report issues at https://github.com/LTMenezes/fluid-playlist/issues
