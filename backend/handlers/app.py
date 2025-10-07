from typing import Annotated
from fastapi import APIRouter, Depends

from backend.schemas import Form, Prediction

from settings import Settings

from backend.service import ClientService
from backend.dependancy import get_client_service, model_predict


router = APIRouter(prefix="/model", tags=["model"])

settings = Settings()
PATH = settings.CLIENT_DATASET_PATH


@router.get(
    '/client_data',
    response_model=Form | str
)
def get_client_data(
        id_client: int,
        client_service: Annotated[ClientService, Depends(get_client_service)]
):
    client_data = client_service.get_client(id_client)
    return client_data


@router.post(
    '/predict',
    response_model=Prediction | str
)
def predict(
        id_client: int,
        client_service: Annotated[ClientService, Depends(get_client_service)]
):
    try:
        form = client_service.get_client(id_client)
        if isinstance(form, Form):
            return model_predict(form)

        return form

    except Exception as e:
        raise e
#
#
# def monitor_model():
#     ...
#
#
# def monitor_target():
#     ...


# if __name__ == "__main__":
#     predict(106805103)

