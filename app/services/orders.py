from sqlalchemy import select
from sqlalchemy.orm import aliased

from .. import db
from .. import models


class CompleteOrdersService:
    @staticmethod
    def get_orders_by_manager_id(manager_id: int) -> list[models.Orders]:
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
                orders_alias.status.is_(True)
            )
        )

        results = db.session.execute(query).fetchall()

        return results
