from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db


class Base(db.Model):
    __abstract__ = True

    def __repr__(self):
        cols = [f'{c} = {getattr(self, c)}' for c in self.__table__.columns.keys()]
        return f'<{self.__class__.__name__} {', '.join(cols)}>'


class Employee(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True)
    post: Mapped[str]
    phone_number: Mapped[str]
    full_name: Mapped[str]
    email: Mapped[str]


class Driver(Base):
    __tablename__ = 'driver'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_type: Mapped[str]
    phone_number: Mapped[str]
    full_name: Mapped[str]


class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str]
    full_name: Mapped[str]
    organization_name: Mapped[str]


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    address: Mapped[str]
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('product.id'))

    product = relationship("Product", back_populates="warehouse")


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    name: Mapped[str]
    price: Mapped[float]
    unit_type: Mapped[str]

    warehouse = relationship("Warehouse", uselist=False, back_populates="product")
