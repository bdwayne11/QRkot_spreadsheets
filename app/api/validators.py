from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_duplicate_name(
        name: str,
        session: AsyncSession
) -> None:
    """Проверка имени на уникальность."""
    project = await charity_project_crud.get_charity_project_by_name(
        name=name, session=session
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверяет, существует ли проект."""
    project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проекта с таким id не существует'
        )
    return project


async def check_project_on_donations_before_delete(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверить, что в проекте уже есть донаты."""
    project = await check_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_project_before_update(
        project_id: int,
        project_in: CharityProjectUpdate,
        session: AsyncSession
) -> CharityProject:
    project = await check_project_exists(
        charity_project_id=project_id, session=session
    )

    if project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )

    if (project_in.full_amount and
            project.invested_amount > project_in.full_amount):
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую cумму меньше уже вложенной'
        )

    await check_duplicate_name(
        name=project_in.name, session=session
    )
    return project
