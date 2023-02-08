from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def invest_close(obj: Union[CharityProject, Donation]) -> None:
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investing_process(session: AsyncSession) -> None:
    """Функция инвестирования."""
    not_closed_donations = await donation_crud.get_not_closed(session)
    not_closed_projects = await charity_project_crud.get_not_closed(session)
    if not all([not_closed_donations, not_closed_projects]):
        return
    for donate in not_closed_donations:
        for project in not_closed_projects:
            money_requested = project.full_amount - project.invested_amount
            money_have = donate.full_amount - donate.invested_amount
            money_diff = money_requested - money_have

            if money_diff > 0:
                project.invested_amount += money_have
                invest_close(donate)

            if money_diff < 0:
                donate.invested_amount += abs(money_diff)
                invest_close(project)

            if money_diff == 0:
                invest_close(project)
                invest_close(donate)

    await session.commit()
