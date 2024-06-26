from fastapi import APIRouter

from .users.handlers import router as users_router
from .packages.handlers import router as tasks_router


router = APIRouter(prefix="/v1")
router.include_router(router=users_router)
router.include_router(router=tasks_router)
