"""API key encryption helpers using Fernet (machine-specific)."""

import base64
import hashlib
import platform

from cryptography.fernet import Fernet

from backend.config import ENCRYPTION_SALT


def _derive_key() -> bytes:
    """Derive a Fernet key from a machine-specific identifier."""
    machine_id = f"{platform.node()}-{platform.machine()}"
    digest = hashlib.pbkdf2_hmac(
        "sha256", machine_id.encode(), ENCRYPTION_SALT, iterations=100_000
    )
    return base64.urlsafe_b64encode(digest)


_fernet = Fernet(_derive_key())


def encrypt_key(plaintext: str) -> str:
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt_key(ciphertext: str) -> str:
    return _fernet.decrypt(ciphertext.encode()).decode()
