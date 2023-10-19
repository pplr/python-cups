#!/usr/bin/env python

import sys
import os
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import basicslib

import ssl
from websockets.sync.client import connect
from cryptography.hazmat.primitives import serialization
import tempfile


def main():
    with open(
        os.path.join(os.path.dirname(__file__), "cups-response.bin"), mode="rb"
    ) as f:
        data = f.read()
    response = basicslib.parseUpdateResponse(data)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.check_hostname = True
    with tempfile.NamedTemporaryFile() as trust, tempfile.NamedTemporaryFile() as pem, tempfile.NamedTemporaryFile() as key:
        pem.write(response.tcCred.cert.public_bytes(serialization.Encoding.PEM))
        pem.flush()
        key.write(
            response.tcCred.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        key.flush()
        trust.write(
            response.tcCred.trust.public_bytes(serialization.Encoding.PEM)
        )
        trust.flush()
        ssl_context.load_verify_locations(trust.name)
        ssl_context.load_cert_chain(
            pem.name,
            key.name,
        )

    with connect(
        uri=response.tcUri + "/router-info", ssl_context=ssl_context
    ) as websocket:
        websocket.send('{"router":"1234:ABCD:FFFF:EEEE"}')
        message = websocket.recv()
        parsed = json.loads(message)
        uri = parsed['uri']
    with connect(
        uri=uri, ssl_context=ssl_context
    ) as websocket:
        websocket.send('{"msgtype":"version","station":"foo","protocol":2,"features":"prod"}')
        message = websocket.recv()
        print(message)
        phy_payload = b'\x40\xC0\x23\x32\x04\x80\x25\x03\x12\xC0\x3C\x22\x02\xE8\x13\xF4\x61\xF4\x3C\xCB\x44\xAB\xCC\x74\xE4\x67\xCF\x64\xA4\x9D\xF0\x02\x9E\xB7\x3F\x41\x06\x53\x88\xE1\x36\xD4\x0D\x91\x09\x23\xB8'
        parsed_payload = basicslib.parsePayload(phy_payload)
        msg = {
            'msgtype':"updf",
            'MHdr': parsed_payload.MHDR,
            'DevAddr': parsed_payload.MACPayload.FHDR.DevAddr,
            'FCtrl': parsed_payload.MACPayload.FHDR.FCtrl,
            'FCnt': parsed_payload.MACPayload.FHDR.FCnt,
            'FOpts': parsed_payload.MACPayload.FHDR.FOpts.hex(),
            'FPort': parsed_payload.MACPayload.FPort,
            'FRMPayload': parsed_payload.MACPayload.FRMPayload.hex(),
            'MIC': parsed_payload.MIC,
            'DR': 0,
            'Freq': 868500000,
            'upinfo': {
                'rctx': 0,
                'xtime': time.time_ns() // 1000,
                'gpstime': 0,
                'rssi': 0,
                'snr': 9.5
            }
        }
        websocket.send(json.dumps(msg))
        message = websocket.recv()
main()
