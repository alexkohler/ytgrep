from ytcc.download import Download
import argparse

parser = argparse.ArgumentParser(description='Ytgrep argument parser')
#TODO wire up to take in url instead of video ID
parser.add_argument('search_query', type=str, help='waskolgi')
parser.add_argument('url', type=str, help='waskolgi')
#parser.add_argument('searchString', metavar='N', type=int, nargs='+', help='revisions')

# don't allow url and regex to be set at same time
args = parser.parse_args()
print(args.search_query)
print(args.url)

#TODO add search args
#TODO improvement - only search text, don't search the timestamp strings

video_id = args.url
download = Download()
captions = download.get_captions(video_id, args.search_query)
print(captions)

# related project: https://github.com/antiboredom/videogrep
# caption downloading: https://github.com/mkly/youtube-closed-captions/tree/master/ytcc
