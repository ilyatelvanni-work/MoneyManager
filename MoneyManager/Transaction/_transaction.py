import datetime as dt

import sqlalchemy as sa

from MoneyManager.db_connection import get_session, Base
from MoneyManager.MyBase import MyBase
from MoneyManager.Category import Category
from MoneyManager.Account import Account


class Transaction(Base, MyBase):

    __tablename__ = 'transaction'

    id = sa.Column(sa.Integer, primary_key=True)
    datetime = sa.Column(sa.DateTime, nullable=False, default=dt.datetime.now)
    value = sa.Column(sa.Numeric(10, 2), nullable=False)
    category_id = sa.Column(sa.Integer, sa.ForeignKey(f'{Category.__tablename__}.id'), nullable=True, default=False)
    account_id = sa.Column(sa.Integer, sa.ForeignKey(f'{Account.__tablename__}.id'), nullable=True, default=False)

    @staticmethod
    async def create(value: float, account_id: int, category_id: int, subcategory_id: int,
                     datetime: str | dt.datetime | None = None) -> None:
        value = int(value)
        account_id = int(account_id)
        category_id = int(category_id)
        subcategory_id = int(subcategory_id)

        if isinstance(datetime, dt.datetime):
            pass
        elif isinstance(datetime, str):
            datetime = dt.datetime.strptime(datetime, '%Y-%m-%dT%H:%M')
        elif datetime is None:
            datetime = dt.datetime.now()
        else:
            assert False, f'datetime in {self.__class__.__name__}.create should be datetime, str or None'

        transaction = Transaction(
            datetime=datetime, value=value, account_id=account_id, category_id=subcategory_id
        )

        async with get_session() as session:
            session.add(transaction)
            await session.commit()

        return transaction

    @staticmethod
    async def get(user_id: int, limit: int | None = None) -> 'Transaction':
        async with get_session() as session:
            result = await session.execute(sa.select(Transaction).limit(limit=limit))
            return result.scalars().all()
