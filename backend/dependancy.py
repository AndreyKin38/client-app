import pandas as pd

from fastapi import APIRouter, Depends

from backend.repository import ClientRepository, ClientCache
from backend.service import ClientService

from backend.database import get_session
from backend.cache import get_redis_connection

from backend.model import get_model
from backend.schemas import Form, Prediction


def get_client_repository() -> ClientRepository:
    db_session = get_session()
    return ClientRepository(db_session)


def get_cache_repository() -> ClientCache:
    redis = get_redis_connection()
    return ClientCache(redis)


def get_client_service(
    client_repository: ClientRepository = Depends(get_client_repository),
    client_cache: ClientCache = Depends(get_cache_repository)
) -> ClientService:
    return ClientService(
        client_repository=client_repository,
        client_cache=client_cache
    )


def model_predict(form: Form) -> Prediction:
    row = pd.DataFrame.from_dict([form.dict()])
    model = get_model()
    prediction = float(model['model'].predict(row)[0])

    return Prediction(
        id_client=form.id_client,
        agreement_rk=form.agreement_rk,
        prediction=prediction
    )


