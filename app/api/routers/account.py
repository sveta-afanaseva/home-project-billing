from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.sql_app import crud, schemas
from app.sql_app.database import get_session

TAG = "accounts"
PREFIX = f"/{TAG}"
router: APIRouter = APIRouter(prefix=PREFIX, tags=[TAG])


def convert_amount(amount: float) -> int:
    """Convert amount from float to int"""
    return int(amount * 100)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create new account",
    response_model=schemas.Account,
)
async def create_account(
    session: AsyncSession = Depends(get_session),
) -> schemas.Account:
    return await crud.create_account(session=session)


@router.put(
    "/{account_id}/top_up",
    status_code=status.HTTP_200_OK,
    summary="Top up account",
    response_model=schemas.Account,
)
async def top_up_account(
    account_id: int,
    amount: int = Depends(convert_amount),
    session: AsyncSession = Depends(get_session),
) -> schemas.Account:
    if not (
        db_account := await crud.get_account(
            session=session,
            account_id=account_id,
            for_update=True,
        )
    ):
        raise HTTPException(status_code=404, detail="Not found")

    return await crud.update_account(
        session=session,
        account_id=account_id,
        new_amount=(db_account.amount + amount),
    )


@router.put(
    "/{account_id}/write_off",
    status_code=status.HTTP_200_OK,
    summary="Write off account",
    response_model=schemas.Account,
)
async def write_off_account(
    account_id: int,
    amount: int = Depends(convert_amount),
    session: AsyncSession = Depends(get_session),
) -> schemas.Account:
    if not (
        db_account := await crud.get_account(
            session=session,
            account_id=account_id,
            for_update=True,
        )
    ):
        raise HTTPException(status_code=404, detail="Not found")

    if (new_amount := (db_account.amount - amount)) < 0:
        raise HTTPException(status_code=409, detail="Insufficient funds")

    return await crud.update_account(
        session=session,
        account_id=account_id,
        new_amount=new_amount,
    )
