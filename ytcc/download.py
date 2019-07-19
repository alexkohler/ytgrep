from __future__ import unicode_literals
import youtube_dl
from pycaption import WebVTTReader
from os import remove
import re
import hashlib
from ytcc.storage import Storage
from colorama import Fore, Style


class Download():
    urls = []
    search_query = ''
    regex = False
    include_links = False

    def __init__(self, args: dict, opts: dict = {}) -> None:
        self.opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'no_warnings': not args['v'],
            'quiet': not args['v'],
        }
        self.urls = args['urls']
        if args['e']:
            self.regex = True
            self.search_query = re.compile(args['pattern'])
        else:
            self.search_query = args['pattern']
        self.opts.update(opts)

        if args.get('links'):
            self.include_links = True

    def get_captions(self) -> str:

        output = ''
        for url in self.urls:
            result = self.get_result(url)
            if result != 0:
                raise Exception(
                    'Unable to download and extract captions: {0}'.format(result))
            storage = Storage(url)
            file_path = storage.get_file_path()
            try:
                with open(file_path) as f:
                    output += self.get_captions_from_output(f.read(), url)
                    storage.remove_file()
            except FileNotFoundError:
                if len(self.urls) == 1:
                    raise NoCaptionsException("no captions found.")
                else:
                    print("WARNING: no captions found for {}".format(url))

        # remove final newline
        if len(output) > 0 and output[-1] == '\n':
            output = output[:-1]
        return output

    def get_result(self, video_id: str) -> int:
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
            
        if self.search_query == '':
            return ''.join(item for item in captions)

        return self.process_captions(captions, url)

    def get_time_url(self, url, time_str):
        h, m, s = time_str.split(':')
        seconds = str(int(h) * 3600 + int(m) * 60 + int(s))
        return url + '&t=' + str(seconds) + 's'

    def process_captions(self, captions, url):
        temp_final = ''
        # if we have multiple urls, print the URL at the beginning
        if len(self.urls) > 1:
            temp_final = url + '\n'
        i = -1
        for caption in captions:
            i += 1
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
                        if Fore.RED + match + Style.RESET_ALL not in stripped:
                            stripped = stripped.replace(
                                match, Fore.RED + match + Style.RESET_ALL)
                            stripped = stripped.replace("'", "").strip()
                    stripped = prefix + stripped
                    if self.include_links:
                        start_time = prefix[1:9]
                        time_url = self.get_time_url(url, start_time)
                        stripped = stripped.rstrip() + ' (' + time_url + ')'
                    temp_final += stripped + '\n'

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
                stripped = stripped.replace("'", "").strip()
                stripped = stripped.replace(
                    self.search_query,
                    Fore.RED +
                    self.search_query +
                    Style.RESET_ALL)
                stripped = prefix + stripped
                if self.include_links:
                    start_time = prefix[1:9]
                    time_url = self.get_time_url(url, start_time)
                    stripped = stripped.rstrip() + ' (' + time_url + ')'
                temp_final += stripped + '\n'

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


class NoCaptionsException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
