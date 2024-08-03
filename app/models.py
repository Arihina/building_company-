from sqlalchemy.orm import Mapped, mapped_column

from . import db


class Base(db.Model):
    __abstract__ = True

    def __repr__(self):
        cols = [f'{c} = {getattr(self, c)}' for c in self.__table__.columns.keys()]
        return f'<{self.__class__.__name__} {', '.join(cols)}>'


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    name: Mapped[str]
    price: Mapped[float]
    unit_type: Mapped[str]
