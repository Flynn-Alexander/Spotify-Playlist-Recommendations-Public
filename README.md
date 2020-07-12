# Spotify-Playlist-Artist-Recommendations
This program uses Spotify's API to analyse a user's Spotify playlist and suggests similar artists that do not appear in the playlist.

Instructions: 
Launch the application 'Spotify-Playlist-Recommendations'. A webpage will open automatically. Follow further instructions
outlined in the 'INSTRUCTIONS' pdf.

Method:
The program collects the recommended artists from each artist in a user's playlist. It compiles these results
and ranks the recommended artists from most recommended to least recommended. This provides a list of
recommended artists that are better catered to the genre/vibe of the playlist.

Plans/Updates:
- Implement automatic authorisation, removing the manual procedure for token retrieval.
- Implement a GUI for improved user experience
- Implement an improved procedure that uses every track on a playlist, removing the 100 track max.

Issues:
- Retrieving the access token manually is a hassle for the user.
- In its current version, the program collects a playlist's artists by looking through a maximum of 100 songs.
A limit of 100 songs is enforced through parameters on the request to Spotify's API. This creates a possibility for some of the 
top recommended artists to already be present on the playlist if the total number of songs on the playlist is greater than 100. 
This is why the program's current version works best on playlists with 100 or less songs. 

