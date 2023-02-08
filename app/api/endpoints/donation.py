from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationAll, DonationCreate, DonationDB
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationAll],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователя."""
    return await donation_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donate(
        donation_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Для авторизированного пользователя."""
    new_donate = await donation_crud.create(
        obj_in=donation_in, session=session, user=user
    )
    await investing_process(session=session)
    await session.refresh(new_donate)
    return new_donate


@router.get(
    '/my',
    response_model=List[DonationDB]
)
async def get_donations_by_user(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Для авторизированного пользователя."""
    return await donation_crud.get_donations_by_user(session=session, user=user)
