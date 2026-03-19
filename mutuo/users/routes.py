from fastapi import APIRouter, Request, Body 

from  mutuo.security.encryption import encrypt, decrypt
from mutuo.security.hashing import hash, deterministic_hash

from .schemas import CreateUser, UserLogin, UserPublic
from .use_cases import create_user, login


router = APIRouter(
    tags=["Users"]
)


@router.post("", status_code=201, response_model=UserPublic)
async def create(
    request: Request,
    data: CreateUser = Body(...)
):
    return await create_user(
        db=request.state.db,
        user_in=data,
        encryption=encrypt,
        decryption=decrypt,
        hash=hash,
        deterministic_hash=deterministic_hash
    )



    