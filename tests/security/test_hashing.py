from mutuo.security.hashing import hash, deterministic_hash, compare_hash


def test_hash():
    data = "hello"

    result = hash(data)

    assert isinstance(result , str)



def test_deterministic_hash():
    data1 = "hello"
    data2 = "hello"

    result1 = deterministic_hash(data=data1)
    result2 = deterministic_hash(data=data2)

    assert result1 == result2


def test_compare_match():
    data = "hello"
    hashed_data = hash(data)

    result = compare_hash(
        "hello",
        hashed_data
    )

    assert result

def test_compare_no_match():
    data = "hello"
    hashed_data = hash(data)

    result = compare_hash(
        "bye",
        hashed_data
    )

    assert not result 