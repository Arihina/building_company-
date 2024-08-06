from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .. import db, logger
from .. import models
from .. import schemas

products_bp = Blueprint('products_bp', __name__)


@products_bp.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        try:
            query = (
                select(models.Product)
            )
            products = db.session.execute(query).scalars().all()
            products_dto = [
                schemas.ProductDto.from_orm(product).dict() for product in products
            ]

            return jsonify(products_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            product_dto = request.get_json()
            product = models.Product(
                name=product_dto['name'],
                type=product_dto['type'],
                price=product_dto['price'],
                unit_type=product_dto['unit_type']
            )

            db.session.add(product)
            db.session.commit()

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


@products_bp.route('/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product(id):
    if request.method == 'GET':
        try:
            product = models.Product.query.get(id)
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            product_dto = schemas.ProductDto.from_orm(product).dict()
            return jsonify({"product": product_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            product = models.Product.query.get(id)

            if not product:
                return jsonify({'error': 'Product not found'}), 404

            product_dto = request.get_json()

            if 'name' in product_dto:
                product.name = product_dto['name']
            if 'type' in product_dto:
                product.type = product_dto['type']
            if 'price' in product_dto:
                product.price = product_dto['price']
            if 'unit_type' in product_dto:
                product.unit_type = product_dto['unit_type']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'DELETE':
        try:
            product = models.Product.query.get(id)
            if product:
                db.session.delete(product)
                db.session.commit()

                return jsonify({'message': 'DELETED'}), 204
            else:
                return jsonify({'error': 'Product not found'}), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
