import os
from typing import Callable, Union
from cryptography.fernet import Fernet
from mutuo.settings import settings


def get_fernet() -> Fernet:
    return Fernet(settings.ENCRYPTION_KEY)


def encrypt(data: str | int) -> str:
    f = get_fernet()
    return f.encrypt(str(data).encode()).decode()


def decrypt(token: str) -> str:
    f = get_fernet()
    return f.decrypt(token.encode()).decode()


EncryptFn = Callable[[Union[str, int]], str]
DecryptFn = Callable[[str], str]