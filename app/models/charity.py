from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.core.db import Base


class CharityBase(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return super().__repr__()


class CharityProject(CharityBase):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f'{super().__repr__()},'
            f'name={self.name},'
            f'description={self.description}'
        )


class Donation(CharityBase):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self) -> str:
        return (
            f'{super().__repr__()},'
            f'user_id={self.user_id},'
            f'comment={self.comment}'
        )
