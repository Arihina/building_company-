from flask import Blueprint, jsonify, request, render_template, abort, flash, redirect, url_for

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

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            flash('Произошла ошибка.', 'error')
            return redirect(url_for('clients_bp.clients'))

    try:
        clients = ClientService.get_clients()
        return render_template('clients.html', clients=clients), 200
    except Exception as ex:
        logger.exception(ex)
        return render_template('500.html'), 500


@clients_bp.route('/clients/<int:id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def client(id):
    logger.debug(f'{request.method} /clients/{id}')
    if request.method == 'GET':
        try:
            client = ClientService.get_client_by_id(id)

            if not client:
                return render_template('404.html'), 404

            client_dto = schemas.ClientDto.from_orm(client).dict()

            return render_template('client_card.html', client=client_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500

    if request.method == 'PUT':
        try:
            status = ClientService.update_client(id, request.get_json())
            if status:
                return jsonify({'message': 'UPDATED'}), 200
            else:
                return render_template('404.html'), 404

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500

    if request.method == 'DELETE':
        try:
            status = ClientService.delete_client(id)
            if status:
                flash('Клиент успешно удалён', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                return render_template('404.html'), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500
