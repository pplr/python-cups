from .utils import *
from .types import *

def parseUpdateResponse (body:bytes) -> 'UpdateInfoResponse':
    seek = 0
    cupsUri, len = readString(body, seek)
    seek += len
    tcUri, len = readString(body, seek)
    seek += len
    cupsCredBin, len = readBlob(body, seek)
    seek += len
    tcCredBin, len = readBlob(body, seek)
    return UpdateInfoResponse(cupsUri, tcUri, parseCreds(cupsCredBin), parseCreds(tcCredBin))
