from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_duplicate_name,
                                check_project_before_update,
                                check_project_on_donations_before_delete)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,

)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Доступно всем пользователям."""
    return await charity_project_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователей."""
    await check_duplicate_name(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project,
                                                    session)
    await investing_process(session=session)
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователей."""
    project = await check_project_on_donations_before_delete(
        charity_project_id=project_id, session=session
    )
    delete_project = await charity_project_crud.delete(
        db_obj=project, session=session
    )
    return delete_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
        project_id: int,
        project_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователей."""
    project = await check_project_before_update(
        project_id=project_id,
        project_in=project_in,
        session=session
    )
    project_update = await charity_project_crud.update(
        db_obj=project, obj_in=project_in, session=session
    )
    return project_update
