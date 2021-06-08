import hashlib
import os
import sys
import unittest

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.TJA import decode_tja, read_tja, parse_tja, set_tja_metadata

# Test data
tja1     = os.path.join(run_path, '..', 'test/data/tja1/test1.tja')
utfbom   = b'\xef\xbb\xbfTITLE:Test1'
shiftjis = b'TITLE:\x90\xe7\x96{\x8d\xf7'

def md5(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.md5(data).hexdigest()


class MyTest(unittest.TestCase):
    def test_0_validate_test_data(self):
        with open(tja1, 'rb') as fh:
            self.assertEqual(md5(fh.read()), '720d7e29b38ba23a9a1b63ee2a827cbd')


    def test_1_decode_tja(self):
        self.assertEqual(decode_tja(shiftjis), 'TITLE:千本桜')
        self.assertEqual(decode_tja(utfbom),   'TITLE:Test1')


    def test_2_read_tja(self):
        result   = read_tja(tja1).encode('utf-8')
        self.assertEqual(md5(result), 'b24996e13bd3fe5a1c48a3d32f783b3a')


    def test_3_parse_tja(self):
        expected = {'title': 'Test1', 'sub': '--Chart test 1', 'bpm': '150', 'song': 'test1.ogg', 'genre': '', 'easy': '3', 'normal': '5', 'hard': '6', 'oni': '7', 'ura': '8'}
        result   = parse_tja(read_tja(tja1))
        self.assertEqual(result, expected)


    def test_4_set_tja_metadata(self):
        tja    = read_tja(tja1)
        result = set_tja_metadata(tja, title="Test x")
        self.assertEqual(md5(result), 'fd14bfedc8ed0d58176c740f5b854e90')

