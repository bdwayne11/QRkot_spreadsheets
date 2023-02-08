from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.charity_project import CharityProject


class CRUDCharityProject(BaseCRUD):

    async def get_charity_project_by_name(
            self,
            name: str,
            session: AsyncSession
    ):
        project = await session.execute(
            select(self.model).where(
                self.model.name == name
            )
        )
        return project.scalars().first()

    async def get_ended_project(
            self,
            session: AsyncSession
    ):
        projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested is True
            )
        )
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
