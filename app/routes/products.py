from flask import Blueprint, abort, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import db, logger
from .. import models
from .. import schemas
from ..models import Product
from ..services.check_post import admin_required

products_bp = Blueprint('products_bp', __name__)


@products_bp.route('/products', methods=['GET', 'POST'])
@login_required
@admin_required
def products():
    logger.debug(f'{request.method} /products')

    if request.method == 'POST':
        try:
            product = models.Product(
                name=request.form.get('name'),
                type=request.form.get('type'),
                price=request.form.get('price'),
                unit_type=request.form.get('unit_type')
            )

            db.session.add(product)
            db.session.commit()

            flash('Товар добавлен успешно', 'success')
            return redirect(url_for('products_bp.products'))

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    try:
        query = (
            select(models.Product)
        )
        products = db.session.execute(query).scalars().all()
        products_dto = [
            schemas.ProductDto.from_orm(product).dict() for product in products
        ]

        return render_template('products.html', products=products_dto), 200

    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@products_bp.route('/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@admin_required
def product(id):
    logger.debug(f'{request.method} /products/{id}')
    if request.method == 'GET':
        try:
            product = models.Product.query.get(id)
            if not product:
                abort(404)

            product_dto = schemas.ProductDto.from_orm(product).dict()
            return render_template('product_card.html', product=product_dto), 200

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'PUT':
        try:
            product = models.Product.query.get(id)

            if not product:
                abort(404)

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
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'DELETE':
        try:
            product = models.Product.query.get(id)
            if product:
                db.session.delete(product)
                db.session.commit()

                flash('Продукт успешно удалён', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                abort(404)
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)


@products_bp.route('/search/products/', methods=['GET'])
@login_required
@admin_required
def search():
    logger.debug(f'{request.method} /search/products/')

    name = request.args.get('name')
    p_type = request.args.get('type')
    price = request.args.get('price')
    unit_type = request.args.get('unit_type')

    query = Product.query

    if name:
        query = query.filter(Product.name == name)
    if p_type:
        query = query.filter(Product.type == p_type)
    if price:
        query = query.filter(Product.price == float(price))
    if unit_type:
        query = query.filter(Product.unit_type == unit_type)

    try:
        filter_products = query.all()
        return render_template('found_products.html', products=filter_products), 200

    except SQLAlchemyError as ex:
        logger.exception(ex)
        abort(500)
