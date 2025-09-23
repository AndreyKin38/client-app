from typing import List

from fastapi import APIRouter, Depends


from backend.schemas import Form, Prediction
from backend.models import Client, Prediction


from sqlalchemy.orm import Session

from backend.db_connection import get_session


router = APIRouter(prefix="/model", tags=["model"])


@router.get('/data', response_model=List[Form])
def get_client_data(limit: int, db: Session = Depends(get_session)):
    query = db.query(Client).limit(limit).all()
    return query


# @router.get('/predict', response_model=Prediction)
# def predict(id_client: int, db: Session = Depends(get_session)):
#     query = db.query(Client).where(Client.ID_CLIENT == id_client).all()
#     return query


def predict(id_client: int):
    db = get_session()
    query = db.query(Client).where(Client.id_client == id_client).scalar()
    print(query.agreement_rk)
    return query


if __name__ == "__main__":
    predict(106805103)

