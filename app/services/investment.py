from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CharityBase,
    CharityProject,
    Donation,
)


async def investment_query(
    session: AsyncSession,
    charity: type[CharityBase]
) -> CharityBase:
    query = await session.execute(
        select(charity)
        .where(charity.fully_invested == 0)
        .order_by('create_date')
    )
    return query.scalars().first()


async def investment_project(
    session: AsyncSession,
    project: CharityProject
) -> CharityProject:
    while not project.fully_invested:
        donation = await investment_query(session, Donation)
        if not donation:
            break
        project.investment(donation)
        session.add(project)
        session.add(donation)
        await session.commit()
        await session.refresh(project)
    return project


async def investment_donation(
    session: AsyncSession,
    donation: Donation
) -> Donation:
    while not donation.fully_invested:
        project = await investment_query(session, CharityProject)
        if not project:
            break
        project.investment(donation)
        session.add(project)
        session.add(donation)
        await session.commit()
        await session.refresh(donation)
    return donation
