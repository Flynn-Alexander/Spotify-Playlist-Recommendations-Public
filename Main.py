#Step 1: Gain authorisation for the spotify API
#Step 2: Grab the list of playlists available
#Step 3: Pick a playlist to receive artist recommendations for
#Step 4: Create a list of artists that feature in the playlist
#Step 5: Create a list of recommended artists
#Step 6: Tally and present the results
#Step 7: Check is user wants to open artist webpage or test another playlist.

import os
import requests
import json
import webbrowser
from collections import Counter

#Functions
# def user_input_int(min,max,prompt):
#     while True:
#         try:
#             user_input = float(input("{}".format(prompt)))
#             if user_input >= min and user_input <= max and (user_input%1) == 0:
#                 break
#         except:
#             pass
#     user_input = int(user_input)    

#     return user_input

def user_input_int(min,max,List,prompt,prompt2):
    #intialisations
    complete = False
    first_call = True
    
    while True:
        #collect user input and check if list input is allowed
        if first_call:
            text = prompt
        else:
            text = prompt2
        while True:
            user_input = input("{}".format(text)).split()
            if List == False and len(user_input) > 1:
                text = prompt2
            else:
                break
        
        #checks
        for i in range(len(user_input)):
            #check for strings
            try:
                user_input[i] = float(user_input[i])
            except: 
                break
            #check against parameters
            if user_input[i] >= min and user_input[i] <= max and (user_input[i]%1) == 0:
                user_input[i] = int(user_input[i])
                if i == (len(user_input)-1):
                    complete = True
            else:
                break
        if complete:
            return user_input

        first_call = False

def yes_or_no(prompt):
    user_input = input("\n{}".format(prompt))
    while True:
        try:
            if user_input == 'y' or user_input == 'Y':
                return True
            elif user_input == 'n' or user_input == 'N':
                return False
            user_input = input("(y/n): ")
        except:
            user_input = input("(y/n): ")

def artist_webpage(query):
    response = requests.get(
        query,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(Token)
            }
    )
    response_json = response.json()
    webbrowser.open("https://open.spotify.com/artist/{}".format(response_json["artists"]["items"][0]["id"]), new = 2, autoraise = True)
    return


#-------------------------------------------------------
#Step 1 - Gain authorisation for the spotify API
#-------------------------------------------------------
webbrowser.open("https://developer.spotify.com/console/get-current-user-playlists/?limit=50&offset=", new = 2, autoraise = True)
Token = input("please input your access token below.\nToken: ")

#-------------------------------------------------------
#Step 2 - Grab the list of playlists available
#-------------------------------------------------------
#send request for current user's playlists.
while True:
    query = "https://api.spotify.com/v1/me/playlists"
    response = requests.get(
            query,
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(Token)
            }
        )
    response_json = response.json()

    #test the token and retrieve list of user's playlists
    try:
        playlists = []
        playlists_ids = []
        for i in range(len(response_json["items"])):
            playlists.append(response_json["items"][i]["name"])
            playlists_ids.append(response_json["items"][i]["id"])
        break
    except:
        Token = input("\nplease input a valid access token below.\nToken: ")


#collect list of user's playlists
playlists = []
playlists_ids = []
for i in range(len(response_json["items"])):
    playlists.append(response_json["items"][i]["name"])
    playlists_ids.append(response_json["items"][i]["id"])

#-------------------------------------------------------
#Step 3 - Pick a playlist to receive artist recommendations for
#-------------------------------------------------------
while True:
    #print the available playlists to pick from
    print("\n")
    for i in range(len(playlists)):
        print("{}.) {}".format(i+1,playlists[i]))

    #get user to pick which playlist to use
    prompt = "\nEnter the number of the playlist you wish to receive Artist recommendations for below.\nPlaylist #: "
    prompt2 = "Playlist #: "
    i = user_input_int(1,(len(playlists)),False,prompt,prompt2) 
    #adjust for indices starting at 0
    i = i[0] - 1
    playlist_id = playlists_ids[i]
    playlist = playlists[i]
        
#-------------------------------------------------------
#Step 4 - Create a list of artists that feature in the playlist
#-------------------------------------------------------
    #send request for items in playlist.
    query = "https://api.spotify.com/v1/playlists/{}/tracks?fields=items(track(artists),total)".format(playlist_id)
    response = requests.get(
        query,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(Token)
        }
    )
    response_json = response.json()

    #collect list of artists (from first 100 songs)
    artists = []
    artists_ids = []
    for i in range(len(response_json["items"])):
        for j in range(len(response_json["items"][i]["track"]["artists"])):
            #checks if artist has a valid id.
            if response_json["items"][i]["track"]["artists"][j-1]["id"] is not None:
                artists.append(response_json["items"][i]["track"]["artists"][j-1]["name"])
                artists_ids.append(response_json["items"][i]["track"]["artists"][j-1]["id"])

    #remove duplicates from the list of artists
    artists = list(set(artists))
    artists_ids = list(set(artists_ids))

#-------------------------------------------------------
#Step 5 - Create a list of recommended artists
#-------------------------------------------------------
    recommended_artists = []
    #collect a list of recommended artists from every artist in the playlist
    print("\nWorking... (typically <30 seconds)")
    for i in range(len(artists_ids)):
        query = "https://api.spotify.com/v1/artists/{}/related-artists".format(artists_ids[i])
        response = requests.get(
        query,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(Token)
        }
        )
        response_json = response.json()

        for j in range(len(response_json["artists"])):
            recommended_artists.append(response_json["artists"][j]["name"])

    #remove original artists from list of recommendations
    for original_artist in artists:
        while True:
            try:
                recommended_artists.remove(original_artist)
            except:
                break

#-------------------------------------------------------
#Step 6 - Tally and present the results
#-------------------------------------------------------
    #prepare the results
    tally = (Counter(recommended_artists)).most_common()
    print("\nFound {} artist recommendations for playlist '{}'".format(len(tally), playlist))
    prompt = "Enter the max number of Artist recommendations you would like to receive below (eg. 20).\nRecommendations: "
    prompt2 = "Recommendations: "
    max_recommendations = user_input_int(1,len(tally),False,prompt, prompt2)
    max_recommendations = max_recommendations[0]

    #present the results 
    print("\nTop recommended Artists for playlist '{}':".format(playlist))
    print("--------------\n# of Recommendations, Artist\n--------------")
    recommendation_counter = 0
    for i in range(max_recommendations):
        print("{}.) {}, {}".format(i+1,tally[i][1],tally[i][0]))
        recommendation_counter += 1

#-------------------------------------------------------
#Step 7 - Check is user wants to open artist webpage or test another playlist.
#-------------------------------------------------------
    #ask the user if they would like to open the webpage of an artist
    prompt = "Would you like to open the webpage for any of these artists? (y/n): "
    response = yes_or_no(prompt)
    if response == True:
        prompt = "\nEnter the number/s of the artist/s you would like to open below. Use a space to separate the numbers (eg. 1 7 11)\nArtist/s #s: "
        prompt2 = "Artist/s #s:" 
        artists_to_open = (user_input_int(1,recommendation_counter,True, prompt, prompt2))
        #adjust for indices starting at 0
        artists_to_open = [x-1 for x in artists_to_open]

        #open the artist/s webpages
        for i in artists_to_open:
            #retrieve the name and id of the artist
            query = "https://api.spotify.com/v1/search?q={}&type=artist&limit=1".format(tally[i][0])
            artist_webpage(query)

    #check if the user would like to test any other playlists
    prompt = "Would you like to repeat this for another playlist? (y/n)"
    if yes_or_no(prompt) == False:
        break