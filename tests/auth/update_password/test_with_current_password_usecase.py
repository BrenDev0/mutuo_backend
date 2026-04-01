import pytest
from unittest.mock import call
from mutuo.auth.usecases import update_password_with_current_password
from mutuo.users.schemas import UserPublic
from mutuo.exceptions import UnauthorizedException, UnprocessableException, NotfoundException

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
    mock_cryptography.hash.return_value = "hashed"

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
    mock_cryptography.hash.assert_called_once_with("new")
    mock_update_user_fn.assert_called_once_with(
        db,
        mock_user.user_id,
        {
            "password": "hashed"
        }
    )


@pytest.mark.asyncio
async def test_user_not_found(
    db,
    mock_user,
    mock_cryptography,
    mock_get_user_by_id_fn,
    mock_update_user_fn,
    mock_update_password_request
):
    mock_get_user_by_id_fn.return_value = None

    with pytest.raises(NotfoundException) as exc_info:
        await update_password_with_current_password(
            db=db,
            user_id=mock_user.user_id,
            cryptography=mock_cryptography,
            get_user_by_id=mock_get_user_by_id_fn,
            update_user=mock_update_user_fn,
            data_in=mock_update_password_request
        )

    assert "User not found" in str(exc_info)
    mock_get_user_by_id_fn.assert_called_once_with(db, mock_user.user_id)
    mock_cryptography.compare_hash.assert_not_called()
    mock_update_user_fn.assert_not_called()
    mock_cryptography.hash.assert_not_called()


@pytest.mark.asyncio
async def test_incorrect_password(
    db,
    mock_user,
    mock_cryptography,
    mock_get_user_by_id_fn,
    mock_update_user_fn,
    mock_update_password_request
):
    mock_get_user_by_id_fn.return_value = mock_user
    mock_cryptography.compare_hash.return_value = False

    with pytest.raises(UnauthorizedException) as exc_info:
        await update_password_with_current_password(
            db=db,
            user_id=mock_user.user_id,
            cryptography=mock_cryptography,
            get_user_by_id=mock_get_user_by_id_fn,
            update_user=mock_update_user_fn,
            data_in=mock_update_password_request
        )

    assert "Incorrect password" in str(exc_info)
    mock_get_user_by_id_fn.assert_called_once_with(db, mock_user.user_id)
    mock_cryptography.compare_hash.assert_called_once_with("current", "hashed")
    mock_update_user_fn.assert_not_called()
    mock_cryptography.hash.assert_not_called()


@pytest.mark.asyncio
async def test_same_as_current_password(
    db,
    mock_user,
    mock_cryptography,
    mock_get_user_by_id_fn,
    mock_update_user_fn,
    mock_update_password_request
):
    mock_get_user_by_id_fn.return_value = mock_user
    mock_cryptography.compare_hash.side_effect = [True, True]

    with pytest.raises(UnprocessableException) as exc_info:
        await update_password_with_current_password(
            db=db,
            user_id=mock_user.user_id,
            cryptography=mock_cryptography,
            get_user_by_id=mock_get_user_by_id_fn,
            update_user=mock_update_user_fn,
            data_in=mock_update_password_request
        )

    assert "New password cannot be same as current password" in str(exc_info)
    mock_get_user_by_id_fn.assert_called_once_with(db, mock_user.user_id)
    mock_cryptography.compare_hash.assert_has_calls([
        call("current", "hashed"),
        call("new", "hashed")
    ])
    mock_update_user_fn.assert_not_called()
    mock_cryptography.hash.assert_not_called()