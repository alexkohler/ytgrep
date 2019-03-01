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
parser.add_argument(
    '-links',
    action="store_true",
    help='include shortcut links to video at matched time i.e. ?t=<time>')
parser.add_argument('pattern', type=str, help='term to search for')
parser.add_argument('urls', nargs='+', help='video URL(s)')

args = parser.parse_args()
args_dict = vars(args)

download = Download(args_dict)
try:
    captions = download.get_captions()
    if len(captions) == 0:
        print("No matches found.")
        sys.exit(1)
    print(captions)
except Exception as err:
    print("Unable to retrieve captions, {}".format(err))

# related project: https://github.com/antiboredom/videogrep
# caption downloading:
# https://github.com/mkly/youtube-closed-captions/tree/master/ytcc


# packaging: https://packaging.python.org/tutorials/packaging-projects/
