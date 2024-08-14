from ..models import Product


class ProductService:
    @staticmethod
    def get_product_by_id(id: int) -> Product:
        return Product.query.get(id)

    @staticmethod
    def get_product_by_name(name: str) -> Product:
        return Product.query().select().where(Product.name == name)
