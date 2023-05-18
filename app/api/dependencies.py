from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.sql_app.crud import AccountRepository
from app.sql_app.database import get_session


async def convert_amount(amount: float) -> int:
    """Convert amount from float to int"""
    return int(amount * 100)


def get_account_repository(
    session: AsyncSession = Depends(get_session),
) -> AccountRepository:
    return AccountRepository(session=session)
