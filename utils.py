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
