import pytest
from unittest.mock import AsyncMock

from mutuo.auth.usecases import login
from mutuo.users.schemas import UserPublic
from mutuo.exceptions import UnauthorizedException


mock_get_by_email_fn = AsyncMock() 

@pytest.mark.asyncio
async def test_success(
    mock_credentials,
    db,
    mock_cryptography,
    mock_user
):
    

    mock_cryptography.compare_hash.return_value = True

    mock_get_by_email_fn.return_value = mock_user 

    result = await login(
        db=db,
        cryptography=mock_cryptography,
        credentials=mock_credentials,
        get_user_by_email_hash=mock_get_by_email_fn
    )


    assert isinstance(result, UserPublic)


@pytest.mark.asyncio
async def test_incorrect_email(
    mock_credentials,
    db,
    mock_cryptography
):
    mock_get_by_email_fn.return_value = None 

    with pytest.raises(UnauthorizedException) as exc:
        await login(
            db=db,
            cryptography=mock_cryptography,
            credentials=mock_credentials,
            get_user_by_email_hash=mock_get_by_email_fn
        )

    assert "Incorrect email or password" in str(exc)


@pytest.mark.asyncio
async def test_incorrect_password(
    mock_credentials,
    db,
    mock_cryptography,
    mock_user
):
    mock_get_by_email_fn.return_value = mock_user
    mock_cryptography.compare_hash.return_value = False

    with pytest.raises(UnauthorizedException) as exc:
        await login(
            db=db,
            cryptography=mock_cryptography,
            credentials=mock_credentials,
            get_user_by_email_hash=mock_get_by_email_fn
        )

    assert "Incorrect email or password" in str(exc)