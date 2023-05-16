from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import insert, select, update

from app.sql_app.models import Account


async def get_account(
    session: AsyncSession,
    account_id: int,
    for_update: bool = False,
) -> Account | None:
    query = select(Account).where(Account.id == account_id)
    if for_update:
        query = query.with_for_update()
    cursor = await session.execute(query)
    account = cursor.scalar()
    return account


async def create_account(session: AsyncSession):
    query = insert(Account).values(amount=0).returning(Account)
    cursor = await session.execute(query)
    account = cursor.scalar()
    await session.commit()
    return {"id": account.id, "amount": account.amount / 100}


async def update_account(session: AsyncSession, account_id: int, new_amount: int):
    query = update(Account).where(Account.id == account_id).values(amount=new_amount)
    await session.execute(query)
    await session.commit()
    return {"id": account_id, "amount": new_amount / 100}
