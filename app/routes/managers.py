from flask import Blueprint, jsonify, request

from .. import db, logger
from .. import models
from .. import schemas
from ..services.clients import ClientService
from ..services.orders import OrdersService

managers_bp = Blueprint('managers_bp', __name__)


# TODO: check user role
@managers_bp.route('/managers/<int:id>', methods=['GET'])
def profile(id):
    logger.debug(f'{request.method} /managers/{id}')
    if request.method == 'GET':
        try:
            manager = models.Employee.query.get(id)
            if not manager:
                return jsonify({'error': 'Manager not found'}), 404

            # if manager.post.lower() != 'менеджер' and manager.post.lower() != 'manager':
            #     return jsonify({'error': 'Forbidden'}), 403

            manager_dto = schemas.ManagerDto.from_orm(manager).dict()

            return jsonify({"manager": manager_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


# TODO: check user role
@managers_bp.route('/managers/<int:id>/orders', methods=['GET', 'POST', 'PUT'])
def processing_orders(id):
    logger.debug(f'{request.method} /managers/{id}/orders')
    # TODO: only orders with status false
    if request.method == 'GET':
        try:
            incomplete_orders = OrdersService.get_orders_by_manager_id(id, False)

            incomplete_orders_dto = [
                schemas.OrderDto(
                    client_name=order.client_name,
                    driver_name=order.driver_name,
                    product_name=order.product_name,
                    product_volume=order.product_volume,
                    data=order.data,
                    deliver_address=order.delivery_address,
                    warehouse_address=order.warehouse_address,
                    order_amount=order.order_amount
                ).dict()
                for order in incomplete_orders
            ]

            return jsonify(incomplete_orders_dto), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            order_dto = schemas.NewOrderDto.model_validate(request.get_json())
            OrdersService.add_order(id, order_dto)

            return jsonify({'message': 'CREATED'}), 201
        except ValueError as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Bad Request', 'message': str(ex)}), 400
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            pass
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


@managers_bp.route('/managers/<int:id>/orders/completes', methods=['GET'])
def completes_orders(id):
    logger.debug(f'{request.method} /managers/{id}/orders/completes')
    if request.method == 'GET':
        try:
            complete_orders = OrdersService.get_orders_by_manager_id(id, True)

            complete_orders_dto = [
                schemas.OrderDto(
                    client_name=order.client_name,
                    driver_name=order.driver_name,
                    product_name=order.product_name,
                    product_volume=order.product_volume,
                    data=order.data,
                    deliver_address=order.delivery_address,
                    warehouse_address=order.warehouse_address,
                    order_amount=order.order_amount
                ).dict()
                for order in complete_orders
            ]

            return jsonify(complete_orders_dto), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


# TODO: check user role
@managers_bp.route('/managers/<int:id>/clients', methods=['GET'])
def managers_clients(id):
    logger.debug(f'{request.method} /managers/{id}/clients')
    if request.method == 'GET':
        try:
            clients = ClientService.get_join_clients(id)

            clients_dto = [
                schemas.ClientJoinDto(
                    full_name=client.full_name,
                    phone_number=client.phone_number,
                    organization_name=client.organization_name
                ).dict()
                for client in clients
            ]

            return jsonify(clients_dto), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
