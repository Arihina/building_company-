from flask import Blueprint, abort, jsonify, request, render_template, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from .. import db, logger
from .. import schemas
from ..services.clients import ClientService

clients_bp = Blueprint('clients_bp', __name__)


@clients_bp.route('/clients', methods=['GET', 'POST'])
def clients():
    logger.debug(f'{request.method} /clients')

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
            return redirect(url_for('clients_bp.clients'))

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    try:
        clients = ClientService.get_clients()
        return render_template('clients.html', clients=clients), 200
    except SQLAlchemyError as ex:
        logger.exception(ex)
        abort(500)


@clients_bp.route('/clients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def client(id):
    logger.debug(f'{request.method} /clients/{id}')
    if request.method == 'GET':
        try:
            client = ClientService.get_client_by_id(id)

            if not client:
                abort(404)

            client_dto = schemas.ClientDto.from_orm(client).dict()

            return render_template('client_card.html', client=client_dto), 200

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'PUT':
        try:
            status = ClientService.update_client(id, request.get_json())
            if status:
                return jsonify({'message': 'UPDATED'}), 200
            else:
                abort(404)

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'DELETE':
        try:
            status = ClientService.delete_client(id)
            if status:
                flash('Клиент успешно удалён', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                abort(404)
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)
