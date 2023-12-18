from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_amount,
    check_closed,
    check_existence,
    check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investment import investment_project

router = APIRouter()


@router.post(
    path='/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charityproject(
    schema: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(schema.name, session)
    project = await charityproject_crud.create(schema, session)
    return await investment_project(session, project)


@router.get(
    path='/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charityprojects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charityproject_crud.get_multi(session)


@router.delete(
    path='/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charityproject(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_existence(project_id, session)
    project = check_amount(project)
    return await charityproject_crud.remove(project, session)


@router.patch(
    path='/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_existence(project_id, session)
    check_closed(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_amount(project, obj_in.full_amount)
    return await charityproject_crud.update(obj_in, project, session)
