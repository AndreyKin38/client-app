import pandas as pd

from sqlalchemy import select, inspect, delete
from sqlalchemy.orm import Session

from backend.models import Client, ClientPredict
from backend.schemas import Form, Prediction


class ClientRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_client_data(self, id_client: int) -> Form | str:
        query = select(Client).where(Client.id_client == id_client)
        with self.db_session as session:
            row = session.execute(query).scalar_one_or_none()
            if row:
                client_data = {c.key: getattr(row, c.key) for c in inspect(row).mapper.column_attrs}
                return Form(**client_data)
            return f"The id_client was not found"

    def create_client(self, client: Form) -> Form:
        with self.db_session as session:
            session.add(client)
            session.commit()

        return client

    def delete_client(self, id_client: int) -> None:
        query = delete(Client).where(Client.id_client == id_client)
        with self.db_session as session:
            session.execute(query)
            session.commit()

    def monitor_model(self):
        ...

    def monitor_target(self):
        ...


