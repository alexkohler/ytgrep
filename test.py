from ytcc.download import Download
import argparse

parser = argparse.ArgumentParser(description='Ytgrep argument parser')
#TODO wire up to take in url instead of video ID
parser.add_argument('--url', type=str, help='waskolgi')
args = parser.parse_args()
#TODO add search args
#TODO improvement - only search text, don't search the timestamp strings

print(args.url)

video_id = '2kREIkF9UAs'
download = Download()
captions = download.get_captions(video_id)
print(captions)

# related project: https://github.com/antiboredom/videogrep
# caption downloading: https://github.com/mkly/youtube-closed-captions/tree/master/ytcc