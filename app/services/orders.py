from sqlalchemy import select
from sqlalchemy.orm import aliased

from .clients import ClientService
from .drivers import DriverService
from .products import ProductService
from .. import db
from .. import models
from ..schemas import NewOrderDto, OrdersDto


class OrdersService:
    @staticmethod
    def get_orders() -> list[dict]:
        query = (
            select(models.Orders)
        )
        orders = db.session.execute(query).scalars().all()
        orders_dto = [
            OrdersDto.from_orm(order).dict() for order in orders
        ]

        return orders_dto

    @staticmethod
    def get_orders_by_manager_id(manager_id: int, status: bool) -> list[models.Orders]:
        employee_alias = aliased(models.Employee)
        client_alias = aliased(models.Client)
        contract_alias = aliased(models.Contract)
        consist_alias = aliased(models.Consist)
        product_alias = aliased(models.Product)
        driver_alias = aliased(models.Driver)
        warehouse_alias = aliased(models.Warehouse)
        orders_alias = aliased(models.Orders)

        query = (
            select(
                client_alias.full_name.label("client_name"),
                orders_alias.id,
                orders_alias.delivery_address,
                orders_alias.product_volume,
                product_alias.name.label("product_name"),
                driver_alias.full_name.label("driver_name"),
                consist_alias.order_amount,
                consist_alias.data,
                warehouse_alias.address.label("warehouse_address")
            )
            .join(contract_alias, orders_alias.contract_id == contract_alias.id)
            .join(employee_alias, contract_alias.employee_id == employee_alias.id)
            .join(client_alias, contract_alias.client_id == client_alias.id)
            .join(consist_alias, contract_alias.contract_consist_id == consist_alias.id)
            .join(product_alias, consist_alias.product_id == product_alias.id)
            .join(driver_alias, orders_alias.driver_id == driver_alias.id)
            .join(warehouse_alias, orders_alias.warehouse_id == warehouse_alias.id)
            .where(
                employee_alias.id == manager_id,
                orders_alias.status.is_(status)
            )
        )

        results = db.session.execute(query).fetchall()

        return results

    @staticmethod
    def add_order(manager_id: int, new_order: NewOrderDto) -> None:
        if new_order.product_id is None and new_order.product_name is None:
            raise ValueError('No data about the product')
        if new_order.client_id is None and new_order.client_name is None:
            raise ValueError('No data about the client')
        if new_order.driver_id is None and new_order.driver_name is None:
            raise ValueError('No data about the driver')

        if new_order.product_id is None:
            new_order.product_id = ProductService.get_product_by_name(new_order.product_name).id
        if new_order.client_id is None:
            new_order.client_id = ClientService.get_client_by_name(new_order.client_name).id
        if new_order.driver_id is None:
            new_order.driver_id = DriverService.get_driver_by_name(new_order.driver_name).id

        consist = models.Consist(
            product_id=new_order.product_id,
            data=new_order.data,
            order_amount=new_order.order_amount,
            account_number=new_order.account_number
        )
        db.session.add(consist)

        contract = models.Contract(
            employee_id=manager_id,
            client_id=new_order.client_id,
            consist=consist
        )
        db.session.add(contract)

        order = models.Orders(
            contract=contract,
            warehouse_id=new_order.warehouse_id,
            delivery_address=new_order.delivery_address,
            driver_id=new_order.driver_id,
            prepayment=new_order.prepayment,
            product_volume=new_order.product_volume,
            status=False
        )
        db.session.add(order)
        db.session.commit()

    @staticmethod
    def get_order_by_id(id: int) -> models.Orders:
        return models.Orders.query.get(id)

    @staticmethod
    def update_order(order_dto: dict, id: int) -> bool:
        order = models.Orders.query.get(id)
        if order:
            if 'contract_id' in order_dto:
                order.contract_id = order_dto['contract_id']
            if 'warehouse_id' in order_dto:
                order.warehouse_id = order_dto['warehouse_id']
            if 'delivery_address' in order_dto:
                order.delivery_address = order_dto['delivery_address']
            if 'driver_id' in order_dto:
                order.driver_id = order_dto['driver_id']
            if 'prepayment' in order_dto:
                order.prepayment = order_dto['prepayment']
            if 'product_volume' in order_dto:
                order.product_volume = order_dto['product_volume']
            if 'status' in order_dto:
                order.status = False if (order_dto['status'] == '0' or order_dto['status'] == 'False') else True
            db.session.commit()

            return True
        else:
            return False

    @staticmethod
    def delete_order(id: int) -> bool:
        order = models.Orders.query.get(id)
        if not order:
            return False
        else:
            db.session.delete(order)
            db.session.commit()
            return True

    @staticmethod
    def get_orders_id_by_manager(manager_id: int) -> list[int]:
        query = (
            select(
                models.Orders.id
            )
            .join(models.Contract, models.Orders.id == models.Contract.id)
            .where(models.Contract.employee_id == manager_id)
        )

        results = db.session.execute(query).fetchall()

        return [row[0] for row in results]
