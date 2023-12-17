from typing import Optional

from pydantic import BaseModel as BaseSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CharityBase,
    User,
)


class CRUDBase:

    def __init__(self, model: CharityBase) -> None:
        self.model = model

    async def create(
        self,
        schema: BaseSchema,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        data = schema.dict()
        if user is not None:
            data['user_id'] = user.id
        result = self.model(**data)
        session.add(result)
        await session.commit()
        await session.refresh(result)
        return result

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(
            select(self.model)
        )
        return db_objs.scalars().all()
