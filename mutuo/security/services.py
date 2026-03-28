from .protocols import CryptographyService
from .types import HashFn, CompareHashFn, DeterministicHashFn, EncryptFn, DecryptFn

class DefaultCryptographyService(CryptographyService):
    def __init__(
        self,
        hash: HashFn,
        deterministic_hash: DeterministicHashFn,
        compare_hash: CompareHashFn,
        encrypt: EncryptFn,
        decrypt: DecryptFn
    ):
        self._hash = hash
        self._deterministic_hash = deterministic_hash
        self._compare_hash = compare_hash
        self._encrypt = encrypt
        self._decrypt = decrypt

    
    def hash(self, str_to_hash: str):
        return self._hash(str_to_hash)
    
    def deterministic_hash(self, value):
        return self._deterministic_hash(value)
    
    def compare_to_hash(self, unhashed: str, hashed: str):
        return self._compare_hash(unhashed, hashed)
    
    def encrypt(self, data: str | int):
        return self._encrypt(data)
    
    def decrypt(self, encrypted: str):
        return self._decrypt(encrypted)