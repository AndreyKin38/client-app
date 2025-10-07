import pandas as pd

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.repository import ClientRepository, ClientCache, UserRepository
from backend.service import ClientService, UserService

from backend.service import ClientService, AuthService

from backend.database import get_session
from backend.cache import get_redis_connection

from backend.model import get_model
from backend.schemas import Form, Prediction

"""CLIENT SERVICE"""


def get_cache_repository() -> ClientCache:
    redis = get_redis_connection()
    return ClientCache(redis)


def get_client_repository(db_session: Session = Depends(get_session)) -> ClientRepository:
    return ClientRepository(db_session=db_session)


def get_client_service(
    client_repository: ClientRepository = Depends(get_client_repository),
    client_cache: ClientCache = Depends(get_cache_repository)
) -> ClientService:
    return ClientService(
        client_repository=client_repository,
        client_cache=client_cache
    )


"""USER SERVICE"""


def get_user_repository(db_session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(
        user_repository=user_repository
    )


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(
        user_repository=user_repository
    )


"""MODEL"""


def model_predict(form: Form) -> Prediction:
    row = pd.DataFrame.from_dict([form.dict()])
    model = get_model()
    prediction = float(model['model'].predict(row)[0])

    return Prediction(
        id_client=form.id_client,
        agreement_rk=form.agreement_rk,
        prediction=prediction
    )


