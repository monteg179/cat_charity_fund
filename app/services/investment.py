from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    CharityBase,
    CharityProject,
    Donation,
)


class Investment:

    @staticmethod
    async def query(session: AsyncSession, charity: type[CharityBase]) -> CharityBase:
        query = await session.execute(
            select(charity)
            .where(charity.fully_invested == 0)
            .order_by('create_date')
        )
        return query.scalars().first()

    @staticmethod
    async def process(session: AsyncSession, charity: CharityBase) -> CharityBase:
        project = await Investment.query(session, CharityProject)
        if not project:
            await session.refresh(charity)
            return charity
        donation = await Investment.query(session, Donation)
        if not donation:
            await session.refresh(charity)
            return charity
        project.investment(donation)
        session.add(project)
        session.add(donation)
        await session.commit()
        return await Investment.process(session, charity)

    @staticmethod
    async def project_process(session: AsyncSession, project: CharityProject) -> CharityProject:
        while not project.fully_invested:
            donation = await Investment.query(session, Donation)
            if not donation:
                break
            project.investment(donation)
            session.add(project)
            session.add(donation)
            await session.commit()
            await session.refresh(project)
        return project

    @staticmethod
    async def donation_process(session: AsyncSession, donation: Donation) -> Donation:
        while not donation.fully_invested:
            project = await Investment.query(session, CharityProject)
            if not project:
                break
            project.investment(donation)
            session.add(project)
            session.add(donation)
            await session.commit()
            await session.refresh(donation)
        return donation
