import pytest
from mutuo.auth.dependencies import user_is_owner
from mutuo.users.schemas import UserPublic
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_success(
    mock_user_public
):

    result = await user_is_owner(
        user=mock_user_public
    )

    assert isinstance(result, UserPublic)


@pytest.mark.asyncio
async def test_unauthorized(
    mock_user_public
):
    mock_user_public.profile_type = "INQUILINO"

    with pytest.raises(HTTPException) as exc_info:
        await user_is_owner(
            user=mock_user_public
        )

    assert "Current profile type is not authorized to create listings" in exc_info.value.detail
    assert exc_info.value.status_code == 403
    