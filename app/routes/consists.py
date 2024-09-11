from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .. import db, logger
from .. import models
from .. import schemas

consists_bp = Blueprint('consists_bp', __name__)


@consists_bp.route('/consists', methods=['GET', 'POST'])
def consists():
    logger.debug(f'{request.method} /consists')
    if request.method == 'GET':
        try:
            query = (
                select(models.Consist)
            )
            consists = db.session.execute(query).scalars().all()
            consists_dto = [
                schemas.ConsistDto.from_orm(consist).dict() for consist in consists
            ]

            return jsonify(consists_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            consist_dto = request.get_json()
            consist = models.Consist(
                data=consist_dto['data'],
                order_amount=consist_dto['order_amount'],
                account_number=consist_dto['account_number'],
                product_id=consist_dto['product_id']
            )

            db.session.add(consist)
            db.session.commit()

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


@consists_bp.route('/consists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def consist(id):
    logger.debug(f'{request.method} /consists/{id}')
    if request.method == 'GET':
        try:
            consist = models.Consist.query.get(id)
            if not consist:
                return jsonify({'error': 'Consist not found'}), 404

            consist_dto = schemas.ConsistDto.from_orm(consist).dict()
            return jsonify({"consist": consist_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            consist = models.Consist.query.get(id)

            if not consist:
                return jsonify({'error': 'Consist not found'}), 404

            consist_dto = request.get_json()

            if 'data' in consist_dto:
                consist.data = consist_dto['data']
            if 'order_amount' in consist_dto:
                consist.order_amount = consist_dto['order_amount']
            if 'account_number' in consist_dto:
                consist.account_number = consist_dto['account_number']
            if 'product_id' in consist_dto:
                consist.product_id = consist_dto['product_id']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'DELETE':
        try:
            consist = models.Consist.query.get(id)
            if consist:
                db.session.delete(consist)
                db.session.commit()

                return jsonify({'message': 'DELETED'}), 204
            else:
                return jsonify({'error': 'Consist not found'}), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
