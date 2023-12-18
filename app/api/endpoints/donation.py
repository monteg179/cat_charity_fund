from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import (
    current_superuser,
    current_user,
)
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationView,
)
from app.services.investment import investment_donation

router = APIRouter()


@router.get(
    path='/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    path='/my',
    response_model=list[DonationView],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_user_donations(user, session)


@router.post(
    path='/',
    response_model=DonationView,
    response_model_exclude_none=True
)
async def create_donation(
    schema: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    donation = await donation_crud.create(schema, session, user)
    return await investment_donation(session, donation)
