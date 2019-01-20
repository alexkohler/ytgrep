from __future__ import unicode_literals
import youtube_dl
from pycaption import WebVTTReader
from os import remove
import re
import hashlib
from urllib.parse import urlencode
from ytcc.storage import Storage
from colorama import Fore, Back, Style


class Download():
    url = ''
    search_query = ''
    regex = False

    def __init__(self, args: dict, opts: dict = {}) -> None:
        self.opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'no_warnings': args['v'],
            'quiet': not args['v'],
        }
        self.url = args['url']
        if args['e']:
            self.regex = True
            self.search_query = re.compile(args['pattern'])
        else:
            self.search_query = args['pattern']
        self.opts.update(opts)

    def get_captions(self, video_id: str) -> str:

        output = ''
        for url in self.url:
            result = self.get_result(url, self.search_query)
            if result != 0:
                raise Exception(
                    'Unable to download and extract captions: {0}'.format(result))
            storage = Storage(url)
            file_path = storage.get_file_path()
            with open(file_path) as f:
                output += self.get_captions_from_output(f.read(), url)
            storage.remove_file()
        return output

    def get_result(self, video_id: str, search_query: str) -> int:
        self.opts['outtmpl'] = 'subtitle_' + \
            hashlib.md5(str(video_id).encode('utf-8')).hexdigest()
        with youtube_dl.YoutubeDL(self.opts) as ydl:
            try:
                return ydl.download([video_id])  # J
            except youtube_dl.utils.DownloadError as err:
                raise DownloadException(
                    "Unable to download captions: {0}".format(str(err)))
            except youtube_dl.utils.ExtractorError as err:
                raise DownloadException(
                    "Unable to extract captions: {0}".format(str(err)))
            except Exception as err:
                raise DownloadException(
                    "Unknown exception downloading and extracting captions: {0}".format(
                        str(err)))

    def get_captions_from_output(self, output: str, url: str) -> str:
        reader = WebVTTReader()

        captions = []
        for caption in reader.read(output).get_captions('en-US'):
            stripped = self.remove_time_from_caption(
                url, str(caption).replace(r'\n', " "))
            stripped += "\n"
            captions.append(stripped)

        return self.process_captions(captions, url)

    def process_captions(self, captions, url):
        temp_final = ''
        # if we have multiple urls, print the URL at the beginning
        if len(self.url) > 1:
            temp_final = url + '\n'
        i = -1
        for caption in captions:
            i += 1
            # TODO figure out whether case insensitivity is something you want
            # to support
            stripped = caption.lower()
            # temporarily remove time prefix via slicing (the time prefix is
            # stable)
            prefix = stripped[0:32]
            stripped = stripped[32:]
            # remove duplicate entries

            if self.regex:
                l = self.search_query.findall(stripped)
                if len(l) > 0:
                    for match in l:
                        stripped = stripped.replace(
                            match, Fore.RED + match + Style.RESET_ALL)
                        stripped = prefix + stripped
                        temp_final += stripped

            elif self.search_query in stripped:

                # It's possible that we have duplicate entries, such as:
                # [00:45:15.960 --> 00:45:15.970] will do this topological sort is what'
                # [00:45:15.970 --> 00:45:20.430] will do this topological sort is what the selvam is usually called topological'
                # so skip the original duplicate if we find a match like this. We trim and ignore quotes to avoid
                # whitespace and quotes from stopping what would otherwise be a
                # match

                if i < len(captions) - 1 and stripped.strip().replace("'",
                                                                      "").replace('"',
                                                                                  '') in str(captions[i + 1]).strip().replace("'",
                                                                                                                              "").replace('"',
                                                                                                                                          ''):
                    continue
                stripped = stripped.replace(
                    self.search_query,
                    Fore.RED +
                    self.search_query +
                    Style.RESET_ALL)
                stripped = prefix + stripped
                temp_final += stripped

        return temp_final

    def remove_time_from_caption(self, video_id: str, caption: str) -> str:
        caption = re.sub(
            r"(\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3})",
            r"[\1]",
            caption,
            flags=re.DOTALL)
        # remove first char from string (will be a quote)
        return caption[1:]


class DownloadException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
