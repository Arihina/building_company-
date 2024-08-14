from sqlalchemy import select
from sqlalchemy.orm import aliased

from .clients import ClientService
from .products import ProductService
from .. import db
from .. import models
from ..schemas import NewOrderDto


class OrdersService:
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

        if new_order.product_id is None:
            new_order.product_id = ProductService.get_product_by_name(new_order.product_name).id
        if new_order.client_id is None:
            new_order.client_id = ClientService.get_client_by_name(new_order.client_name).id

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
            contract_consist_id=consist.id
        )
        db.session.add(contract)

        order = models.Orders(
            contract_id=contract.id,
            warehouse_id=new_order.warehouse_id,
            delivery_address=new_order.delivery_address,
            driver_id=new_order.driver_id,
            prepayment=new_order.prepayment,
            product_volume=new_order.product_volume,
            status=False
        )
        db.session.add(order)
        db.session.commit()
