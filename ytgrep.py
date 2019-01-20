from ytcc.download import Download
import argparse
import sys

parser = argparse.ArgumentParser(description='ytgrep')
parser.add_argument(
    '-e',
    action="store_true",
    help='Interpret PATTERN as an extended regular expression')
parser.add_argument(
    '-v',
    action="store_true",
    help='Print debug information while searching')
parser.add_argument('pattern', type=str, help='term to search for')
parser.add_argument('url', nargs='+', help='video URL')

args = parser.parse_args()
args_dict = vars(args)

# TODO case insensitivity?
# TOOD unit tests

video_id = args.url
download = Download(args_dict)
try:
    captions = download.get_captions(video_id)
    if len(captions) == 0:
        print("No matches found.")
        sys.exit(1)
    print(captions)
except Exception as err:
    print("Unable to retrieve captions {}".format(err))


# related project: https://github.com/antiboredom/videogrep
# caption downloading:
# https://github.com/mkly/youtube-closed-captions/tree/master/ytcc


# packaging: https://packaging.python.org/tutorials/packaging-projects/
