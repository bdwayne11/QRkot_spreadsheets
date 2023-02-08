from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.donation import Donation
from app.models.user import User


class DonationCRUD(BaseCRUD):

    async def get_donations_by_user(self, user: User, session: AsyncSession):
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = DonationCRUD(Donation)
