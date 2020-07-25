import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '0617e5b2a9c540349ea50ca2e3547e8a'
client_secret = '2f254374e3db4c4b9f7f0f38f5cc7554'
client_credentials_manager = SpotifyClientCredentials(
    client_id = client_id, client_secret = client_secret)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

firstsong = sp.search(q="track:" + "CWJBHN", limit = 1, type = "track")

id = firstsong['tracks']['items'][0]['id']
print(id)
name = firstsong['tracks']['items'][0]['name']
print(name)
energy = sp.audio_features([id])[0]['energy']
danceability = sp.audio_features([id])[0]['danceability']
print(energy)
print(danceability)
