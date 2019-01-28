# -*- coding: UTF-8 -*-

import unittest
from ytcc.storage import Storage
from unittest.mock import patch
import hashlib


class TestRemoveFile(unittest.TestCase):

    @patch('os.remove')
    def test_remove_file(self, mock):
        file_path = 'subtitle_' + hashlib.md5('v2309jfGew'.encode('utf-8')).hexdigest() + '.en.vtt'
        video_id = 'v2309jfGew'
        storage = Storage(video_id)
        storage.remove_file()
        mock.assert_called_with(file_path)
