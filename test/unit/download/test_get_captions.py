# -*- coding: UTF-8 -*-

import unittest
from ytcc.download import Download
from unittest.mock import patch, mock_open, Mock
from test.fixtures.webvtt import FIXTURE_WEBVTT
from colorama import Fore, Style
from ytcc.download import NoCaptionsException


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
                'links': False,
                'expected': '[00:00:17.350 --> 00:00:18.752] we have this ' + red('vision') + ' of einstein'
            },
            {
                'name': '1 video, caption not found',
                'urls': ['https://www.swag.com/'],
                'pattern': 'iwontbefound',
                'regex': False,
                'links': False,
                'expected': '',
            },
            {
                'name': '1 video, caption found more than once',
                'urls': ['https://www.swag.com/'],
                'pattern': 'light',
                'regex': False,
                'links': False,
                'expected': '[00:00:33.666 --> 00:00:38.138] actor as einstein: what ' + red('light') + ' would i see if i rode on a beam of ' + red('light') + '?',
            },
            {
                'name': '1 video, regular expression',
                'urls': ['https://www.swag.com/'],
                'pattern': 'actor|light',
                'regex': True,
                'links': False,
                'expected': '[00:00:33.666 --> 00:00:38.138] ' + red('actor') + ' as einstein: what ' + red('light') + ' would i see if i rode on a beam of ' + red('light') + '?',
            },
            {
                'name': '1 video, 1 link',
                'urls': ['https://www.swag.com/'],
                'pattern': 'actor|light',
                'regex': True,
                'links': True,
                'expected': '[00:00:33.666 --> 00:00:38.138] ' + red('actor') + ' as einstein: what ' + red('light') + ' would i see if i rode on a beam of ' + red('light') + '? (https://www.swag.com/&t=33s)',
            },
            # TODO multiple videos and link tag
        ]
        for test in tests:
            download = Download({'urls': test['urls'],
                                 'pattern': test['pattern'],
                                 'e': test['regex'],
                                 'v': False,
                                 'links': test['links']})
            m = mock_open(read_data=FIXTURE_WEBVTT)

            with patch('ytcc.download.open', m, create=True):
                with patch('ytcc.storage.Storage.remove_file', Mock()):
                    download.get_result = Mock(return_value=0)
                    actual = download.get_captions()
                    expected = test['expected']
                    self.assertEqual(actual, expected)

    def test_caption_captions_do_not_exist(self):
        test = {
            'name': 'captions do not exist',
            'urls': ['https://www.swag.com/'],
            'pattern': 'my pattern',
            'regex': False,
            'links': False,
        }

        download = Download({'urls': test['urls'],
                             'pattern': test['pattern'],
                             'e': test['regex'],
                             'v': False,
                             'links': test['links']})
        m = mock_open(read_data=FIXTURE_WEBVTT)
        m.side_effect = FileNotFoundError

        with patch('ytcc.download.open', m, create=True):
            with patch('ytcc.storage.Storage.remove_file', Mock()):
                download.get_result = Mock(return_value=0)
                with self.assertRaises(NoCaptionsException):
                    download.get_captions()
