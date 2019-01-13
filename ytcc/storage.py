# -*- coding: UTF-8 -*-

import re
import os


class Storage():

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id

    def get_file_path(self) -> str:
        video_tag = self.video_id.split("?v=")[1]
        return 'subtitle_{0}.en.vtt'.format(
            re.sub(r'[^\w-]', '', video_tag))

    def remove_file(self) -> None:
        os.remove(self.get_file_path())
