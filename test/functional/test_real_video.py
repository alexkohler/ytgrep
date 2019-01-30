# -*- coding: UTF-8 -*-

import unittest
from ytcc.download import Download, DownloadException, NoCaptionsException
from colorama import Fore, Style


def red(input):
    return Fore.RED + input + Style.RESET_ALL


class TestRealVideo(unittest.TestCase):

    def test_video(self):
        self.download = Download(
            {
                'urls': ['https://www.youtube.com/watch?v=jNQXAC9IVRw'],
                'pattern': 'elephants',
                'e': False,
                'v': False})
        expected = '[00:00:01.300 --> 00:00:04.400] all right, so here we are in front of the ' + \
            red('elephants') + ','
        self.assertEqual(expected, self.download.get_captions())

    def test_video_does_not_exist(self):
        self.download = Download(
            {'urls': ['12323123123'], 'pattern': 'elephants', 'e': False, 'v': False})
        with self.assertRaises(DownloadException):
            self.download.get_captions()
    
    def test_video_no_captions(self):
        self.download = Download(
            {
                'urls': ['https://www.youtube.com/watch?v=jyoTZ69mWZE'],
                'pattern': 'elephants',
                'e': False,
                'v': False})
        with self.assertRaises(NoCaptionsException):
            self.download.get_captions()



class TestMultipleRealVideos(unittest.TestCase):

    def test_video(self):
        self.download = Download(
            {
                'urls': [
                    'https://www.youtube.com/watch?v=jNQXAC9IVRw',
                    'https://www.youtube.com/watch?v=jNQXAC9IVRw'],
                'pattern': 'elephants',
                'e': False,
                'v': False})
        expected = """https://www.youtube.com/watch?v=jNQXAC9IVRw
[00:00:01.300 --> 00:00:04.400] all right, so here we are in front of the elephants,
https://www.youtube.com/watch?v=jNQXAC9IVRw
[00:00:01.300 --> 00:00:04.400] all right, so here we are in front of the elephants,"""
        expected = expected.replace('elephants', red('elephants'))
        self.assertEqual(expected, self.download.get_captions())
    

    def test_video_one_missing_captions(self):
        self.download = Download(
            {
                'urls': [
                    'https://www.youtube.com/watch?v=jNQXAC9IVRw',
                    'https://www.youtube.com/watch?v=jyoTZ69mWZE'],
                'pattern': 'elephants',
                'e': False,
                'v': False})
        expected = """https://www.youtube.com/watch?v=jNQXAC9IVRw
[00:00:01.300 --> 00:00:04.400] all right, so here we are in front of the elephants,"""
        expected = expected.replace('elephants', red('elephants'))
        self.assertEqual(expected, self.download.get_captions())