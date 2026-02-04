from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using Argon2 (argon2-cffi).
    Returns the encoded Argon2 hash string.
    """
    return _ph.hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verify a plaintext password against a stored Argon2 hash.
    Returns True if the password matches, False otherwise.
    """
    try:
        return _ph.verify(stored_hash, password)
    except VerifyMismatchError:
        return False
    except Exception:
        return False
