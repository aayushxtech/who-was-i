import base64
import hashlib

import bcrypt


def _normalize_password(password: str) -> bytes:
    # bcrypt accepts max 72 bytes; pre-hash to fixed length first.
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    # base64 makes bytes printable/stable while staying short.
    return base64.b64encode(digest)


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password must not be empty")

    normalized = _normalize_password(password)
    hashed = bcrypt.hashpw(normalized, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    normalized = _normalize_password(password)
    return bcrypt.checkpw(normalized, password_hash.encode("utf-8"))
