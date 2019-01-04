# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import youtube_dl
from pycaption import WebVTTReader
from os import remove
import re
from urllib.parse import urlencode
from ytcc.storage import Storage


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

    def get_captions(self, video_id: str) -> str:
        result = self.get_result(video_id)

        if result != 0:
            raise Exception(
                'Unable to download and extract captions: {0}'.format(result))

        storage = Storage(video_id)
        file_path = storage.get_file_path()
        with open(file_path) as f:
            output = self.get_captions_from_output(f.read())
        storage.remove_file()
        return output

    def get_result(self, video_id: str) -> int:
        with youtube_dl.YoutubeDL(self.opts) as ydl:
            try:
                return ydl.download([self.get_url_from_video_id(video_id)])
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

    def get_captions_from_output(self, output: str) -> str:
        reader = WebVTTReader()

        temp_final = ''
        for caption in reader.read(output).get_captions('en-US'):
            stripped = self.remove_time_from_caption(
                str(caption).replace(r'\n', " "))
            stripped += "\n"
            temp_final += stripped

        #print(temp_final)

        #final = ''
        #previous = ''
        #for line in temp_final.split("\n"):
        #    if previous != line:
        #        final += "\n" + line
        #    previous = line

        return temp_final #final.replace("\n", ' ')[1:]

    def remove_time_from_caption(self, caption: str) -> str:
        # caption = caption[1:-1]
        #return re.sub(r"^.*?\n", "\n", caption)
        return caption

class DownloadException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
