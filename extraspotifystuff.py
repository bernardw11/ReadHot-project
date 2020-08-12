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


#
# '''testing code below! shit do be working doe.
#
# sampledict = {'man-woman relationships': 3, 'fiction': 3, 'college students': 1,
#     'fiction / contemporary women': 1, 'sexual dominance and submission': 1,
#     'businessmen': 1, 'adultery': 1, 'fiction / romance / contemporary': 1,
#     'dominance (psychology)': 1, 'protected daisy': 1
# }
# bruhid = generate_playlist("fifty shades of grey", "E. L. James","When Anastasia Steele, a young literature student, interviews wealthy young entrepreneur Christian Grey for her campus magazine, their initial meeting introduces Anastasia to an exciting new world that will change them both forever.",
# sampledict, "b")
# '''
#
# '''
# features = {}
# features = get_tone(features, "When Anastasia Steele, a young literature student, interviews wealthy young entrepreneur Christian Grey for her campus magazine, their initial meeting introduces Anastasia to an exciting new world that will change them both forever.")
# print(features)
# # for key in sampledict:
# #     features = get_tone(features, key)
# # print(features)
# final_features = {}
# for feature, levels in features.items():
#     final_features[feature] = sum(levels) / len(levels)
#     if feature == 'valence':
#         final_features[feature] = 1 - final_features[feature]
# print(final_features)
# final_features = squish(final_features)
# print(final_features)
# stuff_id = "50CmpVrHHtTL0e0v2Wvpc4"
# lovetest_id = '1okvjLyiJVXQmxLWMGG9tB'
# happytest_id = '3JlT4kBPE24pPCRr2fiQyZ'
# stuff_songs = get_songs_from_playlist(final_features, lovetest_id)
# #print(stuff_songs)
# print(len(stuff_songs))
# '''

#generate_playlist("fifty shades of grey", "bruh", sampledict)
