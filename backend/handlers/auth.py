from fastapi import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends

from backend.exception import UserNotFoundException, UserIncorrectPasswordException
from backend.schemas import UserLoginSchema, UserCreateSchema

from backend.service import AuthService
from backend.dependancy import get_auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/login', response_model=UserLoginSchema)
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):

    try:
        return auth_service.login(body.user_name, body.password)

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserIncorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )


