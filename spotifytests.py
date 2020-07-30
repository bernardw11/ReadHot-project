import spotipy
import requests
import random

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

client_id = '7c22514bc25d4b2483f5471d9d1b6dc9'
client_secret = '394d743f7c2c4cb591aed988038b5bab'
redirect_uri = 'http://localhost:8888/callback'
scope = "playlist-modify"

sp3 = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope,
    client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, username = "bruh"))
user_id = sp3.current_user()['id']

# Authentication via IAM
authenticator = IAMAuthenticator('GKKyb6SAR11iYpZjZPy9Bnhu3SIC0Nmjc7befjGW3GfV')
service = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator)
ibmurl = "https://api.us-east.tone-analyzer.watson.cloud.ibm.com/instances/748a62e0-af28-4bb9-81a9-c2c325af50c6"
service.set_service_url(ibmurl)

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
    if item['track']:
        id = item['track']['id']
        feature = sp3.audio_features([id])[0][feature]
        return feature
    return 0


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
        if item['track']:
            track = item['track']
            print(f"{idx} {track['artists'][0]['name']} - {track['name']}")
            id = track['id']
            feature_level = sp3.audio_features([id])[0][feature]
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
        feature_level = sp3.audio_features([id])[0][feature]
        print(f"{feature} level: {feature_level}")

#you can make this have a ascending/descending parameter! and then change it so
#ascending_list or descending_list is called, or just make a function called
#sort_items or sort_list that does the whole shebang.
def order_playlist(playlist_name, feature):
    playlists = sp3.current_user_playlists()
    for playlist in playlists['items']:
        name = playlist['name']
        if name == playlist_name:
            id = playlist['id']
            tracks = sp3.playlist_tracks(id)
            descending_list(tracks, feature)
'''
The below code is kinda nifty! allows you to go thru any playlist and
print out the songs in a sorted order.
'''
# playlist_name = input("Enter a playlist name!\n")
# playlist_feature = input("Enter a track feature!\n")
# order_playlist(playlist_name, playlist_feature)


#goes through your entire library to find songs that fit the parameters
def compile_songs_from_library(feature, sign, level):
    all_music = sp3.current_user_saved_tracks(limit = 50)
    total_number = all_music['total']
    list_of_ids = []
    counter = 0
    while counter < total_number and len(list_of_ids) < 100:
        all_music = sp3.current_user_saved_tracks(limit = 50, offset = counter)
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
    new_playlist_id = sp3.user_playlist_create(user_id, new_playlist_name, description = "Created by ReadHot")['id']
    list_of_ids = compile_songs_from_library(feature, sign, level)
    #adds a song
    sp3.user_playlist_add_tracks(user_id, new_playlist_id, list_of_ids)
    return new_playlist_id
    print(f"added new playlist: {new_playlist_name}!")
'''the below code searches thru ur library and creates a playlist!'''
#create_playlist("high acousticness", "acousticness", ">", 0.9)


'''now the real code starts'''



def get_songs_from_playlist(features, playlist_id, difficulty):
    viable_songs = []
    tracklist = sp3.playlist_tracks(playlist_id)
    for idx, item in enumerate(tracklist['items']):
        if item['track']:
            track = item['track']
            #print(f"{idx} {track['artists'][0]['name']} - {track['name']}")
            id = track['id']
            viable = True
            for feature, level in features.items():
                feature_value = sp3.audio_features([id])[0][feature]
                deviation = len(features) * 0.1 * (4 / difficulty)
                if feature_value < (level - deviation) or feature_value > (level + deviation):
                    viable = False
                # else:
                #     print(f"{idx} {track['artists'][0]['name']} - {track['name']} {feature}: {get_feature(item, feature)}")
            if viable:
                viable_songs.append(id)
                # print(f"{track['name']} is viable!")
    return viable_songs

def get_tone(features_dict, text):
    #just for reference
    tone_to_feature = {
        'joy': 'energy',
        'confident': 'danceability',
        'anger': 'valence',
        'fear': 'valence',
        'sadness': 'valence',
        'analytical': 'acousticness',
        'tentative': 'instrumentalness'
    }
    #tones = ['anger', 'fear','joy', 'sadness', 'analytical', 'confident', 'tentative']
    #spotifyfeatures = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'valence', 'tempo']
    tone_input = ToneInput(text)
    tone_dict = service.tone(tone_input=tone_input, content_type="application/json", sentences=False).get_result()
    for tone in tone_dict['document_tone']['tones']:
        tone_name = tone['tone_id']
        feature = tone_to_feature[tone_name]
        if feature in features_dict:
            features_dict[feature].append(tone['score'])
        else:
            feature_vals = []
            feature_vals.append(tone['score'])
            features_dict[feature] = feature_vals
    return features_dict

#
# tone_input = ToneInput('I am very happy. It is a good day.')
# #tone_input = ToneInput('love')
# tone = service.tone(tone_input=tone_input, content_type="application/json", sentences=False).get_result()
# print(tone)

def squish(features_dict):
    output = {}
    for feature, level in features_dict.items():
        if level > 0.5:
            output[feature] = level - ((level - 0.5) / 4)
        else:
            output[feature] = level + ((0.5 - level) / 4)
    return output
# def generate_playlist(title, author, subjects, cover_url):
def generate_playlist(title, author, description, subjects, displayname):
    knownplaylists = {
        'science fiction': ['3Di88mvYplBtkDBIzGLiiM'], #edm
        'romance': ['5KbTzqKBqxQRD8OBtJTZrS', '37i9dQZF1DX50QitC6Oqtn', '37i9dQZF1DX7gIoKXt0gmx'],
        'love': ['5KbTzqKBqxQRD8OBtJTZrS', '37i9dQZF1DX50QitC6Oqtn', '37i9dQZF1DX7gIoKXt0gmx'], #love songs
        'classic': ['3RmQngCZV2qBNXEzMAUKTo'],
        'fantasy': ['1JShdUTOmU54ozm3oZEFMw'],
        'suspense': ['37i9dQZF1DX59NCqCqJtoH', '37i9dQZF1DX4SBhb3fqCJd'],
        'horror': ['37i9dQZF1DX6xZZEgC9Ubl'],
        'dystopia': ['37i9dQZF1DX4OzrY981I1W', '37i9dQZF1DX4SBhb3fqCJd'],
        'action': ['37i9dQZF1DX0XUsuxWHRQd'],
        'mystery': ['37i9dQZF1DX4SBhb3fqCJd'],
        'history': ['37i9dQZF1DX4E3UdUs7fUx'],
        'women': ['6vKtUg0hWDDZvG6eFN7Tde', '37i9dQZF1DX3WvGXE8FqYX']
    }
    moodplaylists = {
        'sad':'37i9dQZF1DWVrtsSlLKzro'
    }

    list_of_song_ids = []

    '''Songs from album is DONE DONE DONE DONE DONE'''
    #gets songs from the official album on spotify
    data = sp3.search(q = title, type = "album")
    albums = data["albums"]
    if albums["items"]:
        albumid = albums["items"][0]["id"]
        print(albumid)
        albumdata = sp3.album_tracks(albumid)
        for track in albumdata['items']:
            list_of_song_ids.append(track['id'])

    '''Songs from description & subjects using tone analyzer'''
    features = {}
    features = get_tone(features, description)
    # for key in subjects:
    #     features = get_tone(features, key)

    final_features = {}
    for feature, levels in features.items():
        final_features[feature] = sum(levels) / len(levels)
        if feature == 'valence':
            final_features[feature] = 1 - final_features[feature]
    final_features = squish(final_features)
    #print(final_features)
    playlistids = []
    #print(subjects)
    for genre in knownplaylists:
        for subject in subjects:
            if genre in subject or genre == subject:
                for id in knownplaylists[genre]:
                    if id not in playlistids:
                        playlistids.append(id)
    # for subject in subjects:
    #     if subject in knownplaylists:
    #         for id in knownplaylists[subject]:
    #             playlistids.append(id)

    cap = len(final_features) * 3
    random.shuffle(playlistids)
    if len(playlistids) > cap:
        playlistids = playlistids[:cap]
    print(playlistids)

    difficulty = len(playlistids)
    for playlistid in playlistids:
        if len(list_of_song_ids) < 100:
            features_songs = get_songs_from_playlist(final_features, playlistid, difficulty)
            for song in features_songs:
                if len(list_of_song_ids) < 100:
                    list_of_song_ids.append(song)

    random.shuffle(list_of_song_ids)
    #print(list_of_song_ids)
    print(len(list_of_song_ids))
    if len(list_of_song_ids) > 30:
        list_of_song_ids = list_of_song_ids[:30]


    new_playlist_id = sp3.user_playlist_create(user_id, f"{title} by {author}", description = f"For {displayname} - Created by ReadHot")['id']
    sp3.user_playlist_add_tracks(user_id, new_playlist_id, list_of_song_ids)
    return new_playlist_id
