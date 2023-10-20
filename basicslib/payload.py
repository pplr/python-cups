from .utils import *
from .types import *
from struct import *

UnconfirmedDataUp = 0b00000010
ConfirmedDataUp = 0b00000100

def parsePayload(data: bytes) -> PHYpayload:
    mhdr,devaddr,fctrl,fcnt = unpack_from("<BiBH", data, 0)
    mtype = MType(mhdr)
    if mtype != UnconfirmedDataUp and mtype != ConfirmedDataUp:
        raise 'Only UnconfirmedDataUp and ConfirmedDataUp are implemented'
    foptslen = FOptsLen(fctrl)
    fopts = data[7:7+foptslen]
    fportAndPayload = data[7+foptslen+1:-4]
    fport = -1
    frmPayload=None
    if len(fportAndPayload) > 1:
        fport, = unpack_from("B", fportAndPayload, 0)
        frmPayload = fportAndPayload[1:]
    mic, = unpack_from("<i", data, len(data) - 4)
    return PHYpayload(
        MHDR=mhdr,
        MIC=mic,
        MACPayload=MACpayload(
            FHDR=Fhdr(
                DevAddr=devaddr,
                FCtrl=fctrl,
                FCnt=fcnt,
                FOpts=fopts
            ),
            FPort=fport,
            FRMPayload=frmPayload,
        ),
    )


def FOptsLen(fctrl: int) -> int:
    return fctrl & 0b00000111

def MType(mhdr: int) -> int:
    return mhdr >> 5