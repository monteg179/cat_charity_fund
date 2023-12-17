from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel as BaseSchema,
    Extra,
    Field,
)


class DonationCreate(BaseSchema):
    full_amount: int = Field(gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationView(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationView):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
