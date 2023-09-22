import datetime as dt
from decimal import Decimal

from MoneyManager.db_connection import Base


class MyBase:

    def as_dict(self) -> dict:
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __json__(self) -> dict:
        dict_ = self.as_dict()
        for key in dict_:
            if isinstance(dict_[key], dt.datetime):
                dict_[key] = dt.datetime.now().strftime('%Y-%m-%dT%H:%M')
            elif isinstance(dict_[key], Decimal):
                dict_[key] = float(dict_[key])
        return dict_

    def __repr__(self) -> str:
        return reduce(
            lambda repr_, el: repr_ + f'{el[0]}={el[1]}', self.as_dict().items(), f'({self.__class__.__name__}'
        ) + ')'
