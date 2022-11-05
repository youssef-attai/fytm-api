from yt_dlp import YoutubeDL

import schemas.track


def youtube_url(watch_id):
    return f'https://youtube.com/watch?v={watch_id}'


def create_track_from_watch_id(watch_id):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'm4a',
        # }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url(watch_id), download=False)

    return schemas.track.Track(
        watch_id=info["id"],
        title=info["title"],
        author=info["channel"],
        thumbnail_url=info["thumbnail"],
        audio_url=info["url"]
    )


def cache_track(watch_id, track_cache_db):
    track_from_yt = create_track_from_watch_id(watch_id).dict(exclude={"__pydantic_initialised__"})
    track_cache_db.insert({
        **track_from_yt
    })
    return track_from_yt


def assert_current_user(current_username, users_db):
    user = users_db.fetch({
        'username': current_username
    }).items

    if len(user) == 0:
        return None
    return user[0]
