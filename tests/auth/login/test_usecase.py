import pytest
from mutuo.auth.usecases import login
from mutuo.users.schemas import UserPublic
from mutuo.exceptions import UnauthorizedException




@pytest.mark.asyncio
async def test_success(
    mock_credentials,
    mock_cryptography,
    mock_user,
    mock_get_user_by_email_hash_fn
):
    
    mock_cryptography.decrypt.return_value = "decrypted"
    mock_cryptography.compare_hash.return_value = True

    mock_get_user_by_email_hash_fn.return_value = mock_user 

    result = await login(
        cryptography=mock_cryptography,
        credentials=mock_credentials,
        get_user_by_email_hash=mock_get_user_by_email_hash_fn
    )


    assert isinstance(result, UserPublic)


@pytest.mark.asyncio
async def test_incorrect_email(
    mock_credentials,
    mock_cryptography,
    mock_get_user_by_email_hash_fn
):
    mock_get_user_by_email_hash_fn.return_value = None 

    with pytest.raises(UnauthorizedException) as exc:
        await login(
            cryptography=mock_cryptography,
            credentials=mock_credentials,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn
        )

    assert "Incorrect email or password" in str(exc)


@pytest.mark.asyncio
async def test_incorrect_password(
    mock_credentials,
    mock_cryptography,
    mock_user,
    mock_get_user_by_email_hash_fn
):
    mock_get_user_by_email_hash_fn.return_value = mock_user
    mock_cryptography.compare_hash.return_value = False

    with pytest.raises(UnauthorizedException) as exc:
        await login(
            cryptography=mock_cryptography,
            credentials=mock_credentials,
            get_user_by_email_hash=mock_get_user_by_email_hash_fn
        )

    assert "Incorrect email or password" in str(exc)