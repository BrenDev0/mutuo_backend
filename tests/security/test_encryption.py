import pytest
from mutuo.security.encryption import decrypt, encrypt
import os
from cryptography.fernet import Fernet


@pytest.fixture(autouse=True)
def set_env():
    os.environ["ENCRYPTION_KEY"] = Fernet.generate_key().decode()


def test_encrypt_decrypt_string():
    data = "test_string"
    encrypted = encrypt(data)
    decrypted = decrypt(encrypted)
    assert decrypted == data

def test_encrypt_decrypt_integer():
    data = 12345
    encrypted = encrypt(data)
    decrypted = decrypt(encrypted)
    assert decrypted == str(data)
