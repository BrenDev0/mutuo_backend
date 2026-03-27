import secrets

def generate_random_code(
    len: int = 6
) -> int:
    min_value = 10 ** (len - 1)
    max_value = (10 ** len) -1

    return secrets.randbelow(max_value - min_value) + min_value