from flask import Blueprint, abort, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from .. import db, logger
from .. import models
from .. import schemas
from ..models import Orders
from ..services.check_post import admin_required
from ..services.orders import OrdersService

orders_bp = Blueprint('orders_bp', __name__)


@orders_bp.route('/orders', methods=['GET', 'POST'])
@login_required
@admin_required
def orders():
    logger.debug(f'{request.method} /orders')

    if request.method == 'POST':
        try:
            order = models.Orders(
                contract_id=request.form.get('contract_id'),
                warehouse_id=request.form.get('warehouse_id'),
                delivery_address=request.form.get('delivery_address'),
                driver_id=request.form.get('driver_id'),
                prepayment=request.form.get('prepayment'),
                product_volume=request.form.get('product_volume'),
                status=False
            )

            db.session.add(order)
            db.session.commit()

            flash('Заказ добавлен успешно', 'success')
            return redirect(url_for('orders_bp.orders'))

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    try:
        return render_template('orders.html', orders=OrdersService.get_orders()), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@orders_bp.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@admin_required
def order(id):
    logger.debug(f'{request.method} /orders/{id}')
    if request.method == 'GET':
        try:
            order = models.Orders.query.get(id)
            if not order:
                abort(404)

            order_dto = schemas.OrdersDto.from_orm(order).dict()
            return render_template('order_card.html', order=order_dto), 200

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'PUT':
        try:
            order_dto = request.get_json()
            status = OrdersService.update_order(order_dto, id)

            if not status:
                abort(404)

            return jsonify({'message': 'UPDATED'}), 200
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'DELETE':
        try:
            status = OrdersService.delete_order(id)
            if status:
                flash('Заказ успешно удалён', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                abort(404)
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)


@orders_bp.route('/search/orders/', methods=['GET'])
@login_required
@admin_required
def search():
    logger.debug(f'{request.method} /search/employees/')

    contract_id = request.args.get('contract_id')
    warehouse_id = request.args.get('warehouse_id')
    driver_id = request.args.get('driver_id')
    delivery_address = request.args.get('delivery_address')
    prepayment = request.args.get('prepayment')
    product_volume = request.args.get('product_volume')

    query = Orders.query

    if contract_id:
        query = query.filter(Orders.contract_id == int(contract_id))
    if warehouse_id:
        query = query.filter(Orders.warehouse_id == int(warehouse_id))
    if driver_id:
        query = query.filter(Orders.driver_id == int(driver_id))
    if delivery_address:
        query = query.filter(Orders.delivery_address == delivery_address)
    if prepayment:
        query = query.filter(Orders.prepayment == float(prepayment))
    if product_volume:
        query = query.filter(Orders.product_volume == int(product_volume))

    try:
        filter_orders = query.all()
        return render_template('found_orders.html', orders=filter_orders), 200

    except SQLAlchemyError as ex:
        logger.exception(ex)
        abort(500)
