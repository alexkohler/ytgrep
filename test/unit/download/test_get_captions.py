# -*- coding: UTF-8 -*-

import unittest
from ytcc.download import Download
from unittest.mock import patch, mock_open, Mock
from test.fixtures.webvtt import FIXTURE_WEBVTT, FIXTURE_WEBVTT_STRIPPED
from colorama import Fore, Back, Style

def red(input):
    return Fore.RED + input + Style.RESET_ALL

class TestCaptions(unittest.TestCase):

    def test_caption(self):
        tests = [
            {
                'name': '1 video, caption found',
                'urls': ['https://www.swag.com/'],
                'pattern': 'vision', 
                'regex': False,
                'expected': '[00:00:17.350 --> 00:00:18.752] we have this ' + red('vision') + ' of einstein'
            },
            {
                'name': '1 video, caption not found',
                'urls': ['https://www.swag.com/'],
                'pattern': 'iwontbefound', 
                'regex': False,
                'expected': '',
            },
            {
                'name': '1 video, caption found more than once',
                'urls': ['https://www.swag.com/'],
                'pattern': 'light', 
                'regex': False,
                'expected': '[00:00:33.666 --> 00:00:38.138] actor as einstein: what ' + red('light') + ' would i see if i rode on a beam of ' + red('light') + '?',
            },
            {
                'name': '1 video, regular expression',
                'urls': ['https://www.swag.com/'],
                'pattern': 'actor|light', 
                'regex': True,
                'expected': '[00:00:33.666 --> 00:00:38.138] ' +  red('actor') + ' as einstein: what ' + red('light') + ' would i see if i rode on a beam of ' + red('light') + '?',
            },
            # TODO multiple videos?
        ]
        for test in tests:
            download = Download({'urls': test['urls'],  'pattern': test['pattern'],'e' : test['regex'],'v': False})
            m = mock_open(read_data=FIXTURE_WEBVTT)

            with patch('ytcc.download.open', m, create=True):
                with patch('ytcc.storage.Storage.remove_file', Mock()):
                    download.get_result = Mock(return_value=0)
                    actual=download.get_captions()
                    expected=test['expected']
                    self.assertEqual(actual, expected)