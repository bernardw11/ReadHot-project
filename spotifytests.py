import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

client_id = '0617e5b2a9c540349ea50ca2e3547e8a'
client_secret = '2f254374e3db4c4b9f7f0f38f5cc7554'
redirect_uri = 'http://127.0.0.1:5000/callback/q'
scope = "user-library-read playlist-modify"

sp2 = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope,
    client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, username = "test_username"))
user_id = sp2.current_user()['id']


#all_music is your library
#all_music['items'] contains all the tracks
#for item in all_music['items']:
#   track = item['track'] is the actual track
#track['id'], track['name'], etc. is all here
#get_feature(item) takes in item, not track.

def get_energy(item):
    return get_feature(item, "energy")
def get_danceability(item):
    return get_feature(item, "danceability")
def get_acousticness(item):
    return get_feature(item, "acousticness")
def get_instrumentalness(item):
    return get_feature(item, "instrumentalness")
def get_valence(item):
    return get_feature(item, "valence")
def get_tempo(item):
    return get_feature(item, "tempo")
#i know, it looks redundant. but this is the only way for sort(key=blah) to work
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
    elif feature == "acousticness":
        tracklist['items'].sort(key = get_acousticness, reverse = True)
    elif feature == "instrumentalness":
        tracklist['items'].sort(key = get_instrumentalness, reverse = True)
    elif feature == "valence":
        tracklist['items'].sort(key = get_valence, reverse = True)
    elif feature == "tempo":
        tracklist['items'].sort(key = get_tempo, reverse = True)
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
    elif feature == "acousticness":
        tracklist['items'].sort(key = get_acousticness)
    #the if statements rly pain me and ill try and figure out a better way.
    #if yall figure out a way to do the above if statements in a better way..
    #like sort(key = get_feature) with parameters, pls lmk!!!
    for idx, item in enumerate(tracklist['items']):
        track = item['track']
        print(f"{idx} {track['artists'][0]['name']} - {track['name']}")
        id = track['id']
        feature_level = sp2.audio_features([id])[0][feature]
        print(f"{feature} level: {feature_level}")

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
'''
The below code is kinda nifty! allows you to go thru any playlist and
print out the songs in a sorted order.
'''
#playlist_name = input("Enter a playlist name!\n")
#playlist_feature = input("Enter a track feature!\n")
#order_playlist(playlist_name, playlist_feature)


#goes through your entire library to find songs that fit the parameters
def compile_songs_from_library(feature, sign, level):
    all_music = sp2.current_user_saved_tracks(limit = 50)
    total_number = all_music['total']
    list_of_ids = []
    counter = 0
    while counter < total_number and len(list_of_ids) < 100:
        all_music = sp2.current_user_saved_tracks(limit = 50, offset = counter)
        for idx, item in enumerate(all_music['items']):
            counter += 1
            track = item['track']
            feature_level = get_feature(item, feature)
            if len(list_of_ids) < 100:
                if sign == "<" and feature_level < level:
                    print(f"{counter}. {track['name']} : {feature_level}")
                    list_of_ids.append(track['id'])
                elif sign == ">" and feature_level > level:
                    print(f"{counter}. {track['name']} : {feature_level}")
                    list_of_ids.append(track['id'])
            else:
                break
    return list_of_ids

#name, feature, >/<, level
#create_playlist(name, feature, >/<. 0-1.0)
def create_playlist(new_playlist_name, feature, sign, level):
    #creates playlist and stores it as new_playlist_id
    new_playlist_id = sp2.user_playlist_create(user_id, new_playlist_name, description = "Created by ReadHot")['id']
    list_of_ids = compile_songs_from_library(feature, sign, level)
    #adds a song
    sp2.user_playlist_add_tracks(user_id, new_playlist_id, list_of_ids)
    return new_playlist_id
    print(f"added new playlist: {new_playlist_name}!")
'''the below code searches thru ur library and creates a playlist!'''
#create_playlist("high acousticness", "acousticness", ">", 0.9)
