# import pytest 
# from unittest.mock import patch
# from mutuo.auth.usecases import update_credentials_with_verification
# from mutuo.auth.schemas import UpdateCredentials

# @pytest.mark.asyncio
# @patch("mutuo.auth.usecases.verify_code_or_raise")
# async def test_update_password_success(
#     mock_verify_code_or_raise,
#     mock_cryptography,
#     mock_get_user_by_email_hash_fn,
#     mock_update_user_fn,
#     db,
#     mock_cache_store,
#     mock_user
# ):
#     mock_cryptography.compare_hash.return_value = False
#     mock_verify_code_or_raise.return_value = None
#     mock_get_user_by_email_hash_fn.return_value

#     mock_changes = UpdateCredentials(
#         password="new"
#     )

#     result = await update_credentials_with_verification(
#         db=db,
#         cache_store=mock_cache_store,
#         changes=mock_changes,
#         cryptography=mock_cryptography,
#         email="email"
#     )

