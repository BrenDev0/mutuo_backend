import pytest
from mutuo.security.encryption import decrypt, encrypt
from mutuo.settings import settings
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
