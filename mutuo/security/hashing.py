import bcrypt
import hashlib
from typing import Callable

def deterministic_hash(data: str) -> str:
        bytes = data.lower().encode('utf-8')  
        hashed_data = hashlib.sha256(bytes).hexdigest()
        return hashed_data


def hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def compare_hash(
    unhashed: str, 
    hashed: str,
) -> bool:
    return bcrypt.checkpw(unhashed.encode('utf-8'), hashed.encode('utf-8'))


type HashFn = Callable[[str], str]
type CompareHashFn = Callable[[str, str], bool]
type DeterministicHashFn = Callable[[str], str]

            