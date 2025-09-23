from typing import List

from fastapi import APIRouter, Depends


from backend.schemas import Form, Prediction
from backend.models import Client, Prediction


from sqlalchemy.orm import Session

from backend.db_connection import get_session

import dill
from model.model_pipe import get_model


router = APIRouter(prefix="/model", tags=["model"])


# def get_model():
#     with open('model/client_pipe.pkl', 'rb') as file:
#         model = dill.load(file)
#
#     return model


# @router.get('/data', response_model=List[Form])
# def get_client_data(limit: int, db: Session = Depends(get_session)):
#     query = db.query(Client).limit(limit).all()
#     return query
#
#
# # @router.get('/predict', response_model=Prediction)
# # def predict(id_client: int, db: Session = Depends(get_session)):
# #     query = db.query(Client).where(Client.ID_CLIENT == id_client).all()
# #     return query
#
# @router.get('/predict', response_model=Prediction)
# def predict(id_client: int):
#     db = get_session()
#     query = db.query(Client).where(Client.id_client == id_client).scalar()
#     print(query.agreement_rk)
#     return query
#
#
# def monitor_model():
#     ...


# def monitor_target():
#     ...
#


if __name__ == "__main__":
    model = get_model()
    print(model['metadata'])

