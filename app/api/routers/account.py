from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import convert_amount, get_account_repository
from app import schemas
from app.db.crud import AccountRepository

TAG = "accounts"
PREFIX = f"/{TAG}"
router: APIRouter = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create new account",
    response_model=schemas.Account,
)
async def create_account(
    repository: AccountRepository = Depends(get_account_repository),
) -> schemas.Account:
    return await repository.create_account()


@router.put(
    "/{account_id}/top_up",
    status_code=status.HTTP_200_OK,
    summary="Top up account",
    response_model=schemas.Account,
)
async def top_up_account(
    account_id: int,
    amount: int = Depends(convert_amount),
    repository: AccountRepository = Depends(get_account_repository),
) -> schemas.Account:
    if not (
        db_account := await repository.get_account(
            account_id=account_id,
            lock=True,
        )
    ):
        raise HTTPException(status_code=404, detail="Not found")

    return await repository.update_account(
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
    repository: AccountRepository = Depends(get_account_repository),
) -> schemas.Account:
    if not (
        db_account := await repository.get_account(
            account_id=account_id,
            lock=True,
        )
    ):
        raise HTTPException(status_code=404, detail="Not found")

    if (new_amount := (db_account.amount - amount)) < 0:
        raise HTTPException(status_code=409, detail="Insufficient funds")

    return await repository.update_account(
        account_id=account_id,
        new_amount=new_amount,
    )
