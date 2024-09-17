from flask import Blueprint, abort, jsonify, request, render_template, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from .. import db, logger
from .. import models
from .. import schemas
from ..services.orders import OrdersService

orders_bp = Blueprint('orders_bp', __name__)


@orders_bp.route('/orders', methods=['GET', 'POST'])
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
