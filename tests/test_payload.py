# -*- coding: utf-8 -*-

import sys
import os
import struct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import basicslib

import unittest
from struct import unpack_from


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
        msg = {
            'msgtype':"updf",
            'MHdr': payload.MHDR,
            'DevAddr': payload.MACPayload.FHDR.DevAddr,
            'FCtrl': payload.MACPayload.FHDR.FCtrl,
            'FCnt': payload.MACPayload.FHDR.FCnt,
            'FOpts': payload.MACPayload.FHDR.FOpts.hex(),
            'FPort': payload.MACPayload.FPort,
            'FRMPayload': payload.MACPayload.FRMPayload.hex(),
            'MIC': payload.MIC,
            'DR': 0,
            'Freq': 868500000,
            'upinfo': {
                'rctx': 0,
                'gpstime': 0,
                'rssi': 0,
                'snr': 9.5
            }
        }
        h = to_hex(msg)
        assert h == '40c023320480250312c03c2202e813f461f43ccb44abcc74e467cf64a49df0029eb73f41065388e136d40d910923b8'


    def test_parse_with_fops(self):
        payload = basicslib.parsePayload(b'\x40\x29\x2E\x01\x26\xFF\x01\x01\x01\x23\x45\x67\x89\xAB\xCD\xEF\xED\xCB\xA9\x87\x65\x43\x21\x00\x00\x01\xC8\x56\x85\xE7\x72\x2E\xFA\xFC\xE6\xC1')
        assert payload.MHDR == 64
        assert payload.MACPayload.FHDR.DevAddr == 637611561
        assert payload.MACPayload.FHDR.FCtrl == 255
        assert payload.MACPayload.FHDR.FCnt == 257
        assert payload.MACPayload.FHDR.FOpts == b'\x01\x23\x45\x67\x89\xAB\xCD\xEF\xED\xCB\xA9\x87\x65\x43\x21'
        assert payload.MACPayload.FPort == 0
        assert payload.MACPayload.FRMPayload == b'\x00\x01\xC8\x56\x85\xE7\x72\x2E'
        assert payload.MIC == -1041826566
        msg = {
            'msgtype':"updf",
            'MHdr': payload.MHDR,
            'DevAddr': payload.MACPayload.FHDR.DevAddr,
            'FCtrl': payload.MACPayload.FHDR.FCtrl,
            'FCnt': payload.MACPayload.FHDR.FCnt,
            'FOpts': payload.MACPayload.FHDR.FOpts.hex(),
            'FPort': payload.MACPayload.FPort,
            'FRMPayload': payload.MACPayload.FRMPayload.hex(),
            'MIC': payload.MIC,
            'DR': 0,
            'Freq': 868500000,
            'upinfo': {
                'rctx': 0,
                'gpstime': 0,
                'rssi': 0,
                'snr': 9.5
            }
        }
        h = to_hex(msg)
        print(h)
        assert h == '40292e0126ff01010123456789abcdefedcba987654321000001c85685e7722efafce6c1'

def to_hex(msg):
    # encode LoRa frame
    mic = msg['MIC']
    mhdr = msg['MHdr']
    devaddr = msg['DevAddr']
    fctrl = msg['FCtrl']
    fcnt = msg['FCnt']
    fopts = bytes.fromhex(msg['FOpts'] if msg['FOpts'] else '')
    fport = bytes.fromhex('%02x' % msg['FPort']  if msg['FPort'] >= 0 else '')
    frmpayload = bytes.fromhex(msg['FRMPayload'] if msg['FRMPayload'] else '')
    LoRaFrame = struct.pack('<BiBH{}s{}s{}si'.format(len(fopts), len(fport), len(frmpayload)),
                mhdr, devaddr, fctrl & 0xFF, fcnt & 0xFFFF, fopts, fport, frmpayload, mic)
    return LoRaFrame.hex()


if __name__ == '__main__':
    unittest.main()