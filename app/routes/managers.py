from datetime import datetime

from flask import Blueprint, abort, request, render_template, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from .. import db, logger
from .. import models
from .. import schemas
from ..services.clients import ClientService
from ..services.drivers import DriverService
from ..services.orders import OrdersService
from ..services.products import ProductService

managers_bp = Blueprint('managers_bp', __name__)


@managers_bp.route('/managers/<int:id>', methods=['GET'])
@login_required
def profile(id):
    logger.debug(f'{request.method} /managers/{id}')

    if id != int(current_user.get_id()):
        abort(403)

    try:
        manager = models.Employee.query.get(id)
        if not manager:
            abort(404)

        manager_dto = schemas.ManagerDto.from_orm(manager).dict()

        return render_template('profile.html', m=manager_dto, id=id)

    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@managers_bp.route('/managers/<int:id>/orders/<int:order_id>', methods=['GET', 'PUT'])
@login_required
def update_order(id, order_id):
    if request.method == 'PUT':
        try:
            order_dto = request.get_json()
            if order_dto['id']:
                if order_dto['id'] in OrdersService.get_orders_id_by_manager(id):
                    order = OrdersService.get_order_by_id(order_dto['id'])
                    if not order:
                        abort(404)

                    OrdersService.update_order(order_dto, order_dto['id'])
                    return jsonify({'message': 'UPDATED'}), 200
                else:
                    abort(403)
            else:
                db.session.rollback()
                abort(400)

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)
    try:
        order = OrdersService.get_order_by_id(order_id)
        if order:
            if order.id not in OrdersService.get_orders_id_by_manager(id):
                abort(403)
            else:
                return render_template('manager_order_card.html', order=order), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@managers_bp.route('/managers/<int:id>/orders', methods=['GET', 'POST'])
@login_required
def processing_orders(id):
    logger.debug(f'{request.method} /managers/{id}/orders')

    if request.method == 'POST':
        try:
            form_data = request.form
            order_dto = schemas.NewOrderDto(
                client_name=form_data['client_name'],
                product_name=form_data['product_name'],
                driver_name=form_data['driver_name'],
                client_id=int(form_data['client_id']),
                product_id=int(form_data['product_id']),
                driver_id=int(form_data['driver_id']),
                warehouse_id=int(form_data['warehouse_id']),
                delivery_address=form_data['delivery_address'],
                data=datetime.strptime(form_data['data'], '%Y-%m-%d'),
                order_amount=float(form_data['order_amount']),
                prepayment=float(form_data['prepayment']),
                account_number=form_data['account_number'],
                product_volume=int(form_data['product_volume'])
            )
            OrdersService.add_order(id, order_dto)

            flash('Заказ добавлен успешно', 'success')

        except ValueError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(400)
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    try:
        incomplete_orders = OrdersService.get_orders_by_manager_id(id, False)

        incomplete_orders_dto = [
            schemas.OrderDto(
                id=order.id,
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

        return render_template('managers_orders.html', orders=incomplete_orders_dto, id=id), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@managers_bp.route('/managers/<int:id>/orders/completes', methods=['GET'])
@login_required
def completes_orders(id):
    logger.debug(f'{request.method} /managers/{id}/orders/completes')

    try:
        complete_orders = OrdersService.get_orders_by_manager_id(id, True)

        complete_orders_dto = [
            schemas.OrderDto(
                id=order.id,
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

        return render_template('orders_compl.html', orders=complete_orders_dto), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@managers_bp.route('/managers/<int:id>/clients', methods=['GET', 'POST'])
@login_required
def managers_clients(id):
    logger.debug(f'{request.method} /managers/{id}/clients')

    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name')
            phone_number = request.form.get('phone_number')
            organization_name = request.form.get('organization_name')

            client_dto = {
                'full_name': full_name,
                'phone_number': phone_number,
                'organization_name': organization_name if organization_name else None
            }
            ClientService.add_client(client_dto)

            flash('Клиент добавлен успешно', 'success')
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

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

        return render_template('clients_list.html', clients=clients_dto, id=id), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@managers_bp.route('/managers/<int:id>/drivers', methods=['GET'])
@login_required
def managers_drivers(id):
    logger.debug(f'{request.method} /managers/{id}/drivers')

    try:
        return render_template('drivers.html', drivers=DriverService.get_drivers()), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@managers_bp.route('/managers/<int:id>/products', methods=['GET'])
@login_required
def managers_products(id):
    logger.debug(f'{request.method} /managers/{id}/products')

    try:
        return render_template('products_list.html',
                               pws=ProductService.get_product_with_warehouses()), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@managers_bp.route('/managers/<int:id>/clients/all', methods=['GET'])
@login_required
def all_clients(id):
    try:
        clients = ClientService.get_clients()
        return render_template('all_clients.html', clients=clients, id=id), 200
    except SQLAlchemyError as ex:
        logger.exception(ex)
        abort(500)
