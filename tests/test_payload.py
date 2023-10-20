# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import basicslib

import unittest


class PayloadTestSuite(unittest.TestCase):
    """Payload test cases."""

    def test_parse(self):
        payload = basicslib.parsePayload(b'\x40\xC0\x23\x32\x04\x80\x25\x03\x12\xC0\x3C\x22\x02\xE8\x13\xF4\x61\xF4\x3C\xCB\x44\xAB\xCC\x74\xE4\x67\xCF\x64\xA4\x9D\xF0\x02\x9E\xB7\x3F\x41\x06\x53\x88\xE1\x36\xD4\x0D\x91\x09\x23\xB8')
        assert payload.MHDR == 64
        assert payload.MACPayload.FHDR.DevAddr == 70394816
        assert payload.MACPayload.FHDR.FCtrl == 128
        assert payload.MACPayload.FHDR.FCnt == 805
        assert payload.MACPayload.FHDR.FOpts == b''
        assert payload.MACPayload.FPort == 18
        assert payload.MACPayload.FRMPayload == b'\xC0\x3C\x22\x02\xE8\x13\xF4\x61\xF4\x3C\xCB\x44\xAB\xCC\x74\xE4\x67\xCF\x64\xA4\x9D\xF0\x02\x9E\xB7\x3F\x41\x06\x53\x88\xE1\x36\xD4\x0D'
        assert payload.MIC == -1205663343


if __name__ == '__main__':
    unittest.main()