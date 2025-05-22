from flask import Flask
from SpotifyAnalyzer.SpotifyAnalyzer import SpotifyAnalyzer


app: Flask = SpotifyAnalyzer.app
# The gooningcorn needs this ):

SpotifyAnalyzer.run()
