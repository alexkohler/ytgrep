# -*- coding: UTF-8 -*-

import re
import os
import hashlib


class Storage():

    def __init__(self, video_url: str) -> None:
        self.video_url = video_url

    def get_file_path(self) -> str:
        return 'subtitle_{0}.en.vtt'.format(re.sub(
            r'[^\w-]', '', hashlib.md5(str(self.video_url).encode('utf-8')).hexdigest()))

    def remove_file(self) -> None:
        os.remove(self.get_file_path())
