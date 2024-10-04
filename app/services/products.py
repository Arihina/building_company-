from sqlalchemy import select

from .. import db
from ..models import Product, Warehouse
from ..schemas import ProductAndWarehouses


class ProductService:
    @staticmethod
    def get_product_by_id(id: int) -> Product:
        return Product.query.get(id)

    @staticmethod
    def get_product_by_name(name: str) -> Product:
        return Product.query().select().where(Product.name == name)

    @staticmethod
    def get_product_with_warehouses() -> list[dict]:
        query = (
            select(
                Product.id, Product.name, Product.type, Product.unit_type,
                Product.price, Warehouse.address, Warehouse.quantity
            )
            .join(Warehouse, Product.id == Warehouse.product_id)
        )

        products = db.session.execute(query).fetchall()

        return [ProductAndWarehouses.from_orm(product).dict() for product in products]

    @staticmethod
    def get_product_with_warehouses_filter(name: str, price: str, quantity: str, address: str, p_type: str) \
            -> list[dict]:
        query = (
            select(
                Product.id, Product.name, Product.type, Product.unit_type,
                Product.price, Warehouse.address, Warehouse.quantity
            )
            .join(Warehouse, Product.id == Warehouse.product_id)
        )

        if name:
            query = query.filter(Product.name == name)
        if price:
            query = query.filter(Product.price == float(price))
        if quantity:
            query = query.filter(Warehouse.quantity == int(quantity))
        if address:
            query = query.filter(Warehouse.address == address)
        if p_type:
            query = query.filter(Product.type == p_type)

        products = db.session.execute(query).fetchall()

        return [ProductAndWarehouses.from_orm(product).dict() for product in products]
