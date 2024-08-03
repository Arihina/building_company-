import datetime

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

    contract = relationship('Contract', back_populates='employee')


class Driver(Base):
    __tablename__ = 'driver'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_type: Mapped[str]
    phone_number: Mapped[str]
    full_name: Mapped[str]

    order = relationship('Orders', back_populates='driver')


class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str]
    full_name: Mapped[str]
    organization_name: Mapped[str]

    contract = relationship('Contract', back_populates='client')


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    address: Mapped[str]
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('product.id'))

    product = relationship('Product', back_populates='warehouse')
    order = relationship('Orders', back_populates='warehouse')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    name: Mapped[str]
    price: Mapped[float]
    unit_type: Mapped[str]

    warehouse = relationship('Warehouse', uselist=False, back_populates='product')
    consists = relationship('Consist', back_populates='product')


class Consist(Base):
    __tablename__ = 'consist'

    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[datetime.datetime]
    order_amount: Mapped[float]
    account_number: Mapped[str]
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('product.id'))

    product = relationship('Product', back_populates='consist')
    contract = relationship('Contract', back_populates='consist')


class Contract(Base):
    __tablename__ = 'contract'

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_consist_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('consist.id'))
    client_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('client.id'))
    employee_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('employee.id'))

    consist = relationship('Consist', back_populates='contract')
    client = relationship('Client', uselist=False, back_populates='contract')
    employee = relationship('Employee', uselist=False, back_populates='contract')
    order = relationship('Orders', back_populates='contract')


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('contract.id'))
    warehouse_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('warehouse.id'))
    driver_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('driver.id'))
    delivery_address: Mapped[str]
    prepayment: Mapped[float]
    product_volume: Mapped[int]
    status: Mapped[bool]

    contract = relationship('Contract', uselist=False, back_populates='orders')
    warehouse = relationship('Warehouse', uselist=False, back_populates='orders')
    driver = relationship('Driver', uselist=False, back_populates='orders')
