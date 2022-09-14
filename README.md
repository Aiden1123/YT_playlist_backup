# YT_playlist_backup
If you are tired of your videos disappearing from yt playlists then this python program is just for you! :)

By simply double-clicking you can create a file containing lists of titles for all your yt playlists so that if a video gets deleted one day you will be able to see what it was called and who uploaded it

Please be aware that:

  -by default the program can only create copies of playlists that are public, however you can manually add non-public playlists by appending strings with their ids to playlist_list. Private playlists cannot be accessed via this program
  
  -you will need to enter your api key in order for this to work [line 7]. If you don't have it you can follow the instructions to get one here: https://developers.google.com/youtube/v3/getting-started
  
  -you will also need to enter your channel id [line 51].
  
  -you will also need python to run the code.
  
Thank you

There is also additional script which will compare files created by the backup script, and will find all videos that have been removed from your playlists (either by you or by other people).

The additional script also tries (in a very basic way) to check if removed video has been added again to the playlist

To use the script place it in the folder with all the generated files and run it. The results will appear in res.txt file. If the file exists it content will be deleted without hesitation
