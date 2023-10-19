from typing import NamedTuple
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes

class Cred(NamedTuple):
    trust: Certificate
    cert: Certificate | None
    key: PrivateKeyTypes | None

OptionalCred = Cred | None

class UpdateInfoResponse(NamedTuple):
    cupsUri: str
    tcUri: str
    cupsCred: OptionalCred
    tcCred: OptionalCred

class Fhdr(NamedTuple):
    DevAddr: int
    FCtrl: int
    FCnt: int
    FOpts: bytes

class MACpayload(NamedTuple):
    FHDR: Fhdr
    FPort: int
    FRMPayload: bytes

class PHYpayload(NamedTuple):
    MHDR: int
    MACPayload: MACpayload
    MIC: int