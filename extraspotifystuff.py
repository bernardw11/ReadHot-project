''' Sorts your first two public playlists in terms of energy!
playlists = sp2.current_user_playlists(limit = 2)
for playlist in playlists['items']:
    id = playlist['id']
    tracks = sp2.playlist_tracks(id)
    least_energy(tracks)
'''


#this is just for reference.
def create_playlist_one_sample():
    new_playlist_id = sp2.user_playlist_create(user_id, new_playlist_name, description = "Created by ReadHot")['id']
    sampletrack = sp2.search(q="track:" + "CWJBHN", limit = 1, type = "track")
    templist_of_tracks = []
    tempid = sampletrack['tracks']['items'][0]['id']
    templist_of_tracks.append(tempid)
    sp2.user_playlist_add_tracks(user_id, new_playlist_id, templist_of_tracks)

# print(lib)
# for track in lib:
#     name = lib['tracks']['items'][0]['name']
#     id = lib['tracks']['items'][0]['id']
#     print(f"{name} - {id}")
'''
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
'''
