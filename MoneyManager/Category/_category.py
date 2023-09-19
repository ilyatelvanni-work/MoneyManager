import sqlalchemy as sa

from MoneyManager.db_connection import get_session, Base
from MoneyManager.MyBase import MyBase

_CATEGORY_TABLE_NAME = 'category'


class Category(Base, MyBase):

    __tablename__ = _CATEGORY_TABLE_NAME

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    is_subcategory = sa.Column(sa.Boolean, nullable=False, default=False)
    is_income = sa.Column(sa.Boolean, nullable=False, default=False)
    parent_category_id = sa.Column(sa.Integer, sa.ForeignKey(f'{_CATEGORY_TABLE_NAME}.id'), index=True)

    async def get() -> 'Category':
        categories_tree = {}

        async with get_session() as session:
            result = await session.execute(sa.select(Category))
            return result.scalars().all()
