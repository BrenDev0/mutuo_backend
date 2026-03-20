from fastapi import APIRouter

from mutuo.users.routes import router as users_router
from mutuo.auth.routes import router as auth_router

router = APIRouter()


router.include_router(auth_router, prefix="/auth")
router.include_router(users_router, prefix="/users")