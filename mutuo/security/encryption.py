import os
from typing import Callable, Union
from cryptography.fernet import Fernet


def get_fernet() -> Fernet:
    key = os.getenv("ENCRYPTION_KEY")
    if key is None:
        raise ValueError("Encryption variables not set")
    return Fernet(key)


def encrypt(data: str | int) -> str:
    f = get_fernet()
    return f.encrypt(str(data).encode()).decode()


def decrypt(token: str) -> str:
    f = get_fernet()
    return f.decrypt(token.encode()).decode()


EncryptFn = Callable[[Union[str, int]], str]
DecryptFn = Callable[[str], str]