from typing import Callable, Union

EncryptFn = Callable[[Union[str, int]], str]
DecryptFn = Callable[[str], str]


HashFn = Callable[[str], str]
CompareHashFn = Callable[[str, str], bool]
DeterministicHashFn = Callable[[str], str]