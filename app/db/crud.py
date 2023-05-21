from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import insert, select, update

from app.db.models import Account


class AccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_account(
        self,
        account_id: int,
        lock: bool = False,
    ) -> Account | None:
        query = select(Account).where(Account.id == account_id)
        if lock:
            query = query.with_for_update()
        cursor = await self.session.execute(query)
        account = cursor.scalar()
        return account

    async def create_account(self):
        query = insert(Account).values(amount=0).returning(Account)
        cursor = await self.session.execute(query)
        account = cursor.scalar()
        await self.session.commit()
        return {"id": account.id, "amount": account.amount / 100}

    async def update_account(self, account_id: int, new_amount: int):
        query = (
            update(Account).where(Account.id == account_id).values(amount=new_amount)
        )
        await self.session.execute(query)
        await self.session.commit()
        return {"id": account_id, "amount": new_amount / 100}
