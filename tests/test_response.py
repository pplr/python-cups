# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import basicslib

import unittest


class UpdateInfoResponseTestSuite(unittest.TestCase):
    """UpdateInfoResponse test cases."""

    def test_parse_empty(self):
        response = basicslib.parseUpdateResponse(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        assert response.cupsUri == ""
        assert response.tcUri == ""
        assert response.cupsCred == None
        assert response.tcCred == None

    def test_parse_non_empty(self):
        with open(os.path.join(os.path.dirname(__file__), 'cups-response.bin'), mode="rb") as f:
            data = f.read()
        response = basicslib.parseUpdateResponse(data)
        assert response.cupsUri == ""
        assert response.tcUri == "wss://lns.thingpark.com:443"
        assert response.cupsCred.trust.serial_number == 143266978916655856878034712317230054538369994
        assert response.cupsCred.cert == None
        assert response.cupsCred.key == None

        assert response.tcCred.trust.serial_number == 15288609957017289050
        assert response.tcCred.cert.serial_number == 8724105900870385099
        assert response.tcCred.key != None


if __name__ == '__main__':
    unittest.main()