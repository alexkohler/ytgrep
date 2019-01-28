# -*- coding: UTF-8 -*-

import unittest
from ytcc.storage import Storage
import hashlib


class TestGetFilePath(unittest.TestCase):


    def test_valid(self):
        video_id = 'jNQXAC9IVRw'
        hashed_video_id = hashlib.md5(video_id.encode('utf-8')).hexdigest()
        storage = Storage(video_id)
        expected = 'subtitle_{0}.en.vtt'.format(hashed_video_id)
        self.assertEqual(expected, storage.get_file_path())

