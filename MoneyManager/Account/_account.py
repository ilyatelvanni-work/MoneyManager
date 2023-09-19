import sqlalchemy as sa

from MoneyManager.db_connection import get_session, Base
from MoneyManager.MyBase import MyBase
from MoneyManager.Currency import Currency


class Account(Base, MyBase):

    __tablename__ = 'account'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    user_id = sa.Column(sa.Integer, nullable=False)
    currency_id = sa.Column(sa.Integer, sa.ForeignKey(f'{Currency.__tablename__}.id'), nullable=False)
    initial_balance = sa.Column(sa.Numeric(10, 2), nullable=False, default=0)

    async def get() -> 'Account':
        categories_tree = {}

        async with get_session() as session:
            result = await session.execute(sa.select(Account))
            return result.scalars().all()
