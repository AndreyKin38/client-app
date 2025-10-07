from typing import Annotated
from fastapi import APIRouter, Depends

from backend.schemas import UserLoginSchema, UserCreateSchema

from backend.service import UserService
from backend.dependancy import get_user_service


router = APIRouter(prefix="/user", tags=["user"])


@router.post('/login', response_model=UserLoginSchema)
async def create_user(
        body: UserCreateSchema,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    return user_service.create_user(body.user_name, body.password)
