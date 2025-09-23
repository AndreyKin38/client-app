from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import ForeignKey

from backend.db_connection import Base


class Client(Base):
    __tablename__ = 'clients'
    __table_args__ = {'schema': 'public'}

    age = Column(Integer)
    gender = Column(Integer)
    education = Column(String)
    marital_status = Column(String)
    child_total = Column(Integer)
    dependants = Column(Integer)
    socstatus_work_fl = Column(Integer)
    socstatus_pens_fl = Column(Integer)
    reg_address_province = Column(String)
    fact_address_province = Column(String)
    postal_address_province = Column(String)
    fl_presence_fl = Column(Integer)
    own_auto = Column(Integer)
    family_income = Column(String)
    personal_income = Column(Float)
    id_client = Column(Integer,
                       primary_key=True)
    gen_industry = Column(String)
    gen_title = Column(String)
    job_dir = Column(String)
    work_time = Column(Float)
    credit = Column(Float)
    term = Column(Integer)
    fst_payment = Column(Float)
    loan_count = Column(Integer)
    closed_fl = Column(Integer)
    agreement_rk = Column(Integer,
                          ForeignKey('public.predictions.id_client'),
                          primary_key=True)
    target = Column(Integer)


class Prediction(Base):
    __tablename__ = 'predictions'
    __table_args__ = {'schema': 'public'}

    id_client = Column(Integer,
                       primary_key=True)
    agreement_rk = Column(Integer,
                          ForeignKey('public.clients.id_client'),
                          primary_key=True)
    prediction = Column(Float)


# if __name__ == "__main__":
#     session = SessionLocal()
#     result = (
#         session.query(Client)
#         .filter(Client.reg_address_province == 'Московская область')
#         .limit(5)
#         .all()
#     )
#
#     for client in result:
#         print(client.id_client)
#         print(client.age)
#         print(client.personal_income)
#         print()






