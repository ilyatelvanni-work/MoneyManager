from MoneyManager.db_connection import Base


class MyBase:

    def as_dict(self) -> dict:
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __json__(self) -> dict:
        return self.as_dict()

    def __repr__(self) -> str:
        return reduce(
            lambda repr_, el: repr_ + f'{el[0]}={el[1]}', self.as_dict().items(), f'(self.__class__.__name__'
        ) + ')'
