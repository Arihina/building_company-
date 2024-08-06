from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .. import db
from .. import models
from .. import schemas

clients_bp = Blueprint('clients_bp', __name__)


@clients_bp.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'GET':
        try:
            query = (
                select(models.Client)
            )
            clients = db.session.execute(query).scalars().all()
            clients_dto = [
                schemas.ClientDto.from_orm(client).dict() for client in clients
            ]

            return jsonify(clients_dto), 200

        except Exception as ex:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            client_dto = request.get_json()
            client = models.Client(
                full_name=client_dto['full_name'],
                phone_number=client_dto['phone_number'],
                organization_name=client_dto['organization_name']
            )

            db.session.add(client)
            db.session.commit()

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


@clients_bp.route('/clients/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def client(id):
    if request.method == 'GET':
        try:
            client = models.Client.query.get(id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404

            client_dto = schemas.ClientDto.from_orm(client).dict()
            return jsonify({"client": client_dto}), 200

        except Exception as ex:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            client = models.Client.query.get(id)

            if not client:
                return jsonify({'error': 'Client not found'}), 404

            client_dto = request.get_json()

            if 'full_name' in client_dto:
                client.full_name = client_dto['full_name']
            if 'phone_number' in client_dto:
                client.phone_number = client_dto['phone_number']
            if 'organization_name' in client_dto:
                client.organization_name = client_dto['organization_name']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except Exception as ex:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'DELETE':
        try:
            client = models.Client.query.get(id)
            if client:
                db.session.delete(client)
                db.session.commit()

                return jsonify({'message': 'DELETED'}), 204
            else:
                return jsonify({'error': 'Client not found'}), 404
        except Exception as ex:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
