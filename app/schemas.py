from pydantic import BaseModel


class Account(BaseModel):
    id: int
    amount: float
