from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .. import db, logger
from .. import models
from .. import schemas
from ..services.orders import OrdersService

orders_bp = Blueprint('orders_bp', __name__)


# TODO: refactor with using services layer


@orders_bp.route('/orders', methods=['GET', 'POST'])
def orders():
    logger.debug(f'{request.method} /orders')
    if request.method == 'GET':
        try:
            query = (
                select(models.Orders)
            )
            orders = db.session.execute(query).scalars().all()
            orders_dto = [
                schemas.OrdersDto.from_orm(order).dict() for order in orders
            ]

            return jsonify(orders_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            order_dto = request.get_json()
            order = models.Orders(
                contract_id=order_dto['contract_id'],
                warehouse_id=order_dto['warehouse_id'],
                delivery_address=order_dto['delivery_address'],
                driver_id=order_dto['driver_id'],
                prepayment=order_dto['prepayment'],
                product_volume=order_dto['product_volume'],
                status=order_dto['status']
            )

            db.session.add(order)
            db.session.commit()

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


@orders_bp.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def order(id):
    logger.debug(f'{request.method} /orders/{id}')
    if request.method == 'GET':
        try:
            order = models.Orders.query.get(id)
            if not order:
                return jsonify({'error': 'Order not found'}), 404

            order_dto = schemas.OrdersDto.from_orm(order).dict()
            return jsonify({"order": order_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            order = models.Orders.query.get(id)

            if not order:
                return jsonify({'error': 'Order not found'}), 404

            order_dto = request.get_json()
            OrdersService.update_order(order_dto, id)

            return jsonify({'message': 'UPDATED'}), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'DELETE':
        try:
            order = models.Orders.query.get(id)
            if order:
                db.session.delete(order)
                db.session.commit()

                return jsonify({'message': 'DELETED'}), 204
            else:
                return jsonify({'error': 'Order not found'}), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
