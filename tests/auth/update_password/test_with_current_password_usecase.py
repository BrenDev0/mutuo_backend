import pytest
from unittest.mock import call
from mutuo.auth.usecases import update_password_with_current_password
from mutuo.users.schemas import UserPublic

@pytest.mark.asyncio
async def test_success(
    db,
    mock_user,
    mock_cryptography,
    mock_get_user_by_id_fn,
    mock_update_user_fn,
    mock_update_password_request
):
    mock_get_user_by_id_fn.return_value = mock_user
    mock_cryptography.compare_hash.side_effect = [True, False]
    mock_update_user_fn.return_value = mock_user

    result = await update_password_with_current_password(
        db=db,
        user_id=mock_user.user_id,
        cryptography=mock_cryptography,
        get_user_by_id=mock_get_user_by_id_fn,
        update_user=mock_update_user_fn,
        data_in=mock_update_password_request
    )

    assert isinstance(result, UserPublic)
    mock_get_user_by_id_fn.assert_called_once_with(db, mock_user.user_id)
    mock_cryptography.compare_hash.assert_has_calls([
        call(mock_update_password_request.current_password, mock_user.password),
        call(mock_update_password_request.new_password, mock_user.password)
    ])
    mock_update_user_fn.assert_called_once_with(
        db,
        mock_user.user_id,
        {
            "password": "hashed"
        }
    )




    
    