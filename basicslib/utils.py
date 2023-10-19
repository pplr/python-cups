from struct import *
from .types import *
from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.primitives.serialization import load_der_private_key

def readString(data: bytes, pos: int) -> (str, int):
    b, len = readSmallblob(data, pos)
    return b.decode("utf-8"), len


def readSmallblob(data: bytes, pos: int) -> (bytes, int):
    return _readBlob(data, pos, "B", 1)


def readBlob(data: bytes, pos: int) -> (bytes, int):
    return _readBlob(data, pos, "H", 2)


def _readBlob(data: bytes, pos: int, lenghtType: str, lengthSize: int) -> (bytes, int):
    (len,) = unpack_from(f"<{lenghtType}", data, pos)
    format = f"{len}s"
    return unpack_from(format, data, pos + lengthSize)[0], len + lengthSize


def parseCreds(data: bytes) -> OptionalCred:
    if data == b"":
        return None
    seek = 0
    trust, len = readAsnSeq(data, seek)
    seek += len
    cert, len = readAsnSeqOrNoData(data, seek)
    seek += len
    key = readKey(data, seek)
    
    return Cred(
        trust=trust,
        cert=cert,
        key=key,
    )

def readKey(data, pos) -> PrivateKeyTypes | None:
    keyBin = data[pos:]
    if keyBin == b'\x00\x00\x00\x00':
        return None
    else:
        return load_der_private_key(keyBin, None)

def readAsnSeqOrNoData(data: bytes, pos: int) -> (Certificate | None, int):
    if data[pos] == 0x00:
        return None, 4
    else:
        return readAsnSeq(data, pos)


def readAsnSeq(data: bytes, pos: int) -> (Certificate, int):
    if isSeq(data, pos):
        len = seqLen(data, pos)
        end = pos + len
        return load_der_x509_certificate(data[pos:end]), len
    else:
        raise "ASN.1 SEQ expected"


def isSeq(data: bytes, pos: int) -> bool:
    return data[pos] == 0x30


def seqLen(data: bytes, pos: int) -> int:
    if data[pos + 1] & 0x80:
        return (((data[pos + 2] & 0xFF) << 8) | (data[pos + 3] & 0xFF)) + 4
    else:
        return data[pos + 1] + 2
