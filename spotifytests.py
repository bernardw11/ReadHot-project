import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

client_id = '0617e5b2a9c540349ea50ca2e3547e8a'
client_secret = '2f254374e3db4c4b9f7f0f38f5cc7554'
redirect_uri = 'http://127.0.0.1:5000/callback/q'
scope = "user-library-read playlist-modify"

sp2 = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope,
    client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, username = "bernardohiggins11"))
user_id = sp2.current_user()['id']
print(f"user id: {user_id}")

def get_energy(item):
    id = item['track']['id']
    energy = sp2.audio_features([id])[0]['energy']
    return energy
def get_danceability(item):
    id = item['track']['id']
    danceability = sp2.audio_features([id])[0]['danceability']
    return danceability

#im not sure how to implement this yet. alas!
def get_feature(item, feature):
    id = item['track']['id']
    feature = sp2.audio_features([id])[0][feature]
    return feature


#next step: store the items in order instead of simply printing the feature's
#level! store them in order by id. so then you can take the top 10 id's or so.
#and then finally we can add them to a playlist yayyy!!
def descending_list(tracklist, feature):
    #since i dont know how to sort with get_feature(item, feature),
    #i have a bunch of if statements. unfortunate. don't think it's possible.
    if feature == "energy":
        tracklist['items'].sort(key = get_energy, reverse = True)
    elif feature == "danceability":
        tracklist['items'].sort(key = get_danceability, reverse = True)
    #the if statements rly pain me and ill try and figure out a better way.
    #if yall figure out a way to do the above if statements in a better way..
    #like sort(key = get_feature) with parameters, pls lmk!!!
    for idx, item in enumerate(tracklist['items']):
        track = item['track']
        print(f"{idx} {track['artists'][0]['name']} - {track['name']}")
        id = track['id']
        feature_level = sp2.audio_features([id])[0][feature]
        print(f"{feature} level: {feature_level}")

def ascending_list(tracklist, feature):
    #SAME DEAL WITH THIS FUNCTION!!! LITERALLY ALL WE REMOVE IS reverse = True

    #since i dont know how to sort with get_feature(item, feature),
    #i have a bunch of if statements. unfortunate. don't think it's possible.
    if feature == "energy":
        tracklist['items'].sort(key = get_energy)
    elif feature == "danceability":
        tracklist['items'].sort(key = get_danceability)
    #the if statements rly pain me and ill try and figure out a better way.
    #if yall figure out a way to do the above if statements in a better way..
    #like sort(key = get_feature) with parameters, pls lmk!!!
    for idx, item in enumerate(tracklist['items']):
        track = item['track']
        print(f"{idx} {track['artists'][0]['name']} - {track['name']}")
        id = track['id']
        feature_level = sp2.audio_features([id])[0][feature]
        print(f"{feature} level: {feature_level}")

''' Sorts your first two public playlists in terms of energy!
playlists = sp2.current_user_playlists(limit = 2)
for playlist in playlists['items']:
    id = playlist['id']
    tracks = sp2.playlist_tracks(id)
    least_energy(tracks)
'''

#you can make this have a ascending/descending parameter! and then change it so
#ascending_list or descending_list is called, or just make a function called
#sort_items or sort_list that does the whole shebang.
def order_playlist(playlist_name, feature):
    playlists = sp2.current_user_playlists()
    for playlist in playlists['items']:
        name = playlist['name']
        if name == playlist_name:
            id = playlist['id']
            tracks = sp2.playlist_tracks(id)
            descending_list(tracks, feature)

playlist_name = input("Enter a playlist name!\n")
playlist_feature = input("Enter a track feature!\n")
order_playlist(playlist_name, playlist_feature)

def create_playlist(new_playlist_name):
    new_playlist_id = sp2.user_playlist_create(user_id, new_playlist_name, description = "ayooooo this got created w the mf api")['id']
    sampletrack = sp2.search(q="track:" + "CWJBHN", limit = 1, type = "track")

    templist_of_tracks = []
    tempid = sampletrack['tracks']['items'][0]['id']
    templist_of_tracks.append(tempid)
    sp2.user_playlist_add_tracks(user_id, new_playlist_id, templist_of_tracks)
    print(f"added new playlist: {new_playlist_name}!")

create_playlist("testing testing")

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
