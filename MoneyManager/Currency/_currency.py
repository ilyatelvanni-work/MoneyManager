import sqlalchemy as sa

from MoneyManager.db_connection import get_session, Base
from MoneyManager.MyBase import MyBase


class Currency(Base, MyBase):

    __tablename__ = 'currency'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    short_name = sa.Column(sa.String(3), nullable=False)

    @staticmethod
    async def get() -> 'Currency':
        async with get_session() as session:
            result = await session.execute(sa.select(Currency))
            return result.scalars().all()
