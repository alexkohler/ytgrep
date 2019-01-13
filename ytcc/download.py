# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import youtube_dl
from pycaption import WebVTTReader
from os import remove
import re
from urllib.parse import urlencode
from ytcc.storage import Storage
from colorama import Fore, Back, Style


class Download():
    base_url = 'http://www.youtube.com/watch'

    def __init__(self, opts: dict = {}) -> None:
        self.opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'outtmpl': 'subtitle_%(id)s'
        }
        self.opts.update(opts)

    def update_opts(self, opts: dict) -> None:
        self.opts.update(opts)

    def get_captions(self, video_id: str, search_query: str) -> str:
        result = self.get_result(video_id, search_query)

        if result != 0:
            raise Exception(
                'Unable to download and extract captions: {0}'.format(result))

        storage = Storage(video_id)
        file_path = storage.get_file_path()
        with open(file_path) as f:
            output = self.get_captions_from_output(f.read(), video_id, search_query)
        storage.remove_file()
        return output

    def get_result(self, video_id: str, search_query : str) -> int:
        with youtube_dl.YoutubeDL(self.opts) as ydl:
            try:
                return ydl.download([video_id])#J
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

    def get_url_from_video_id(self, video_id: str) -> str:
        return '{0}?{1}'.format(self.base_url, urlencode({'v': video_id}))

    def get_captions_from_output(self, output: str, video_id: str, search_query: str) -> str:
        reader = WebVTTReader()

        temp_final = ''
        #TODO allow regular expressions
        matches=[]
        for caption in reader.read(output).get_captions('en-US'):
            stripped = self.remove_time_from_caption(video_id, 
                str(caption).replace(r'\n', " "))
            stripped += "\n"
            #temp_final += stripped
            if search_query in stripped:
                stripped=stripped.replace(search_query,  Fore.RED + search_query + Style.RESET_ALL)
                temp_final += stripped

        return temp_final #final.replace("\n", ' ')[1:]

    def remove_time_from_caption(self, video_id: str, caption: str) -> str:
        #TODO sanitize intervals to remove duplicate noise (if a line is already taken care of by an interval, don't bother)

        # todo embed link here?
        #begin=caption[2:9]
        #h, m, s = begin.split(':')
        #seconds= int(h) * 3600 + int(m) * 60 + int(s)
        #timeURL=video_id + '?t={}'.format(seconds)
        #print(timeURL)

        caption = re.sub(r"(\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3})", r"[\1]", caption, flags=re.DOTALL)
        # caption = caption + '(' + timeURL + ')'
        # grab first x characters to get timestamp - TODO should this be done in a cleaner way?
        # remove first char from string
        return caption[1:]

class DownloadException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
