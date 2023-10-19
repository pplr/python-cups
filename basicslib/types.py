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