from pydantic import BaseModel, Field, model_validator


class Form(BaseModel):
    age: int
    gender: int
    education: str
    marital_status: str
    child_total: int
    dependants: int
    socstatus_work_fl: int
    socstatus_pens_fl: int
    reg_address_province: str
    fact_address_province: str
    postal_address_province: str
    fl_presence_fl: int
    own_auto: int | None
    family_income: str | None
    personal_income: float
    id_client: int
    gen_industry: str | None
    gen_title: str | None
    job_dir: str | None
    work_time: float | None
    credit: float | None
    term: int | None
    fst_payment: float | None
    loan_count: int | None
    closed_fl: int | None
    agreement_rk: int
    target: int

    class Config:
        from_attributes = True


class Prediction(BaseModel):
    id_client: int
    rk: int | None = Field(alias='agreement_rk')
    # agreement_rk: int = Field(exclude=True)
    prediction: float

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_agreement_rk(self):
        if self.rk is None:
            raise ValueError("agreement_rk must be provided")

        return self


