#!/usr/bin/env python

import sys
import os

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
        print(f"Received: {message}")


main()
