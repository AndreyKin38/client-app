import dill
import pandas as pd
from fastapi import APIRouter

from backend.schemas import Form, Prediction, Client, ClientPredict
from .db_connection import get_session
from backend.preprocess.preprocessors import ClientDataset, DropDuplicatesAndOutliers
from backend.model import get_model

router = APIRouter(prefix="/model", tags=["model"])

# @router.get('/data', response_model=List[Form])
# def get_client_data(limit: int, db: Session = Depends(get_session)):
#     query = db.query(Client).limit(limit).all()
#     return query


PATH = 'backend/data/client_dataset.csv'


@router.get('/row', response_model=Form | str)
def get_client_data(id_client: int):
    db = get_session()
    try:
        query = db.query(Client).where(Client.id_client == id_client).scalar()
        if query:
            return query.__dict__
        else:
            return f'The id_client was not found'

    except Exception as e:
        raise e


@router.post('/data', response_model=Prediction)
def predict(form: Form):

    row = pd.DataFrame.from_dict([form.dict()])

    try:
        model = get_model()
        prediction = float(model['model'].predict(row)[0])
        return Prediction(
            id_client=form.id_client,
            prediction=prediction
        )

    except Exception as e:
        raise e


#     d = query.__dict__
#     del d['_sa_instance_state']
#     data = pd.DataFrame([d])
#     print(data)

    # model = get_model()
    # pred = model['model'].predict(data)
    # print(pred)
    # return Prediction(
    #     id_client=None,
    #     agreement_rk=None,
    #     prediction=None
    # )


def monitor_model():
    ...


def monitor_target():
    ...


# if __name__ == "__main__":
#     predict(106805103)

