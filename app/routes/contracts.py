from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .. import db, logger
from .. import models
from .. import schemas

contracts_bp = Blueprint('contracts_bp', __name__)


@contracts_bp.route('/contracts', methods=['GET', 'POST'])
def contracts():
    logger.debug(f'{request.method} /contracts')
    if request.method == 'GET':
        try:
            query = (
                select(models.Contract)
            )
            contracts = db.session.execute(query).scalars().all()
            contracts_dto = [
                schemas.ContractDto.from_orm(contract).dict() for contract in contracts
            ]

            return jsonify(contracts_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            contract_dto = request.get_json()
            contract = models.Contract(
                contract_consist_id=contract_dto['contract_consist_id'],
                client_id=contract_dto['client_id'],
                employee_id=contract_dto['employee_id']
            )

            db.session.add(contract)
            db.session.commit()

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


@contracts_bp.route('/contracts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def contract(id):
    logger.debug(f'{request.method} /contracts/{id}')
    if request.method == 'GET':
        try:
            contract = models.Contract.query.get(id)
            if not contract:
                return jsonify({'error': 'Contract not found'}), 404

            contract_dto = schemas.ContractDto.from_orm(contract).dict()
            return jsonify({"contract": contract_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            contract = models.Contract.query.get(id)

            if not contract:
                return jsonify({'error': 'Contract not found'}), 404

            contract_dto = request.get_json()

            if 'contract_consist_id' in contract_dto:
                contract.contract_consist_id = contract_dto['contract_consist_id']
            if 'client_id' in contract_dto:
                contract.client_id = contract_dto['client_id']
            if 'employee_id' in contract_dto:
                contract.employee_id = contract_dto['employee_id']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'DELETE':
        try:
            contract = models.Contract.query.get(id)
            if contract:
                db.session.delete(contract)
                db.session.commit()

                return jsonify({'message': 'DELETED'}), 204
            else:
                return jsonify({'error': 'Contract not found'}), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
