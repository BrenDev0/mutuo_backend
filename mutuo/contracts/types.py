from typing import Callable, Awaitable

from .models import ContractPartial, Contract

CreateContractFn = Callable[[ContractPartial], Awaitable[Contract]]