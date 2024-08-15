from flask import Blueprint, jsonify, request

from .. import db, logger
from .. import schemas
from ..services.clients import ClientService

clients_bp = Blueprint('clients_bp', __name__)


@clients_bp.route('/clients', methods=['GET', 'POST'])
def clients():
    logger.debug(f'{request.method} /clients')

    if request.method == 'GET':
        try:
            return jsonify(ClientService.get_clients()), 200

        except Exception as ex:
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            ClientService.add_client(request.get_json())

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


# TODO: check user role
@clients_bp.route('/clients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def client(id):
    logger.debug(f'{request.method} /clients/{id}')
    if request.method == 'GET':
        try:
            client = ClientService.get_client_by_id(id)

            if not client:
                return jsonify({'error': 'Client not found'}), 404

            client_dto = schemas.ClientDto.from_orm(client).dict()

            return jsonify({"client": client_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            status = ClientService.update_client(id, request.get_json())
            if status:
                return jsonify({'message': 'UPDATED'}), 200
            else:
                return jsonify({'error': 'Client not found'}), 404

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'DELETE':
        try:
            status = ClientService.delete_client(id)
            if status:
                return jsonify({'message': 'DELETED'}), 204
            else:
                return jsonify({'error': 'Client not found'}), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
