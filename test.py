from ytcc.download import Download

video_id = '2kREIkF9UAs'
download = Download()
captions = download.get_captions(video_id)
print(captions)