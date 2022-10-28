# Free YouTube Music API

This API allows you to stream music from YouTube for free.

## How it works

Users can search for their favorite _tracks_ and get links to
audio files that can be used in media streaming.

If they 
could not find the track they are looking for, 
they can add it to the app by providing the track's metadata
(e.g. the title, artist, album, etc.)
and the YouTube video ID
(i.e. the gibberish after **v=** in: https://www.youtube.com/watch?v=dQw4w9WgXcQ).

The added tracks are saved to the database, so that everyone can find them next time
they search for them.

Users can do the same with _artists_ and _albums_.

They can also create an account, to create their personal _playlists_.

****

<a href="https://geaajs.deta.dev/docs">
<img src="./imgs/try-it-out-button.png" width="125px"/>
</a>

****

**🚧 This API is still under development**

- [x] Add new tracks, artists, and albums.
- [x] Search for tracks, artists, and albums.
- [x] Create an account.
- [x] Add tracks to personal playlist.
- [ ] Get direct link to track audio for streaming.
- [ ] Add track cover, album cover, and artist picture.
- [ ] Add categories to tracks.
