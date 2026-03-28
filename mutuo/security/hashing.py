import bcrypt
import hashlib

def deterministic_hash(value: str) -> str:
        bytes = value.lower().encode('utf-8')  
        hashed_data = hashlib.sha256(bytes).hexdigest()
        return hashed_data


def hash(str_to_hash: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(str_to_hash.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def compare_hash(
    unhashed: str, 
    hashed: str,
) -> bool:
    return bcrypt.checkpw(unhashed.encode('utf-8'), hashed.encode('utf-8'))

            