# Luigi UI

Web interface to start [Luigi](https://github.com/spotify/luigi/) tasks.

## Installation

Install [Flask](http://flask.pocoo.org/):

    pip install flask

Then, start server:

    python server.py

## Configuration

Set the names of the Python packages to be loaded in [`config.json`](config.json).

By default, Luigi UI runs on port 5000, but you can change this by editing [`config.json`](config.json) or by setting the `PORT` environment variable.
