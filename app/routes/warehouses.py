from flask import Blueprint, jsonify, request
from sqlalchemy import select

from .. import db, logger
from .. import models
from .. import schemas

warehouses_bp = Blueprint('warehouses_bp', __name__)


# TODO: check user role
@warehouses_bp.route('/warehouses', methods=['GET', 'POST'])
def warehouses():
    logger.debug(f'{request.method} /warehouses')
    if request.method == 'GET':
        try:
            query = (
                select(models.Warehouse)
            )
            warehouses = db.session.execute(query).scalars().all()
            warehouses_dto = [
                schemas.WarehouseDto.from_orm(warehouse).dict() for warehouse in warehouses
            ]

            return jsonify(warehouses_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'POST':
        try:
            warehouse_dto = request.get_json()
            warehouse = models.Warehouse(
                quantity=warehouse_dto['quantity'],
                address=warehouse_dto['address'],
                product_id=warehouse_dto['product_id']
            )

            db.session.add(warehouse)
            db.session.commit()

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500


# TODO: check user role
@warehouses_bp.route('/warehouses/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def warehouse(id):
    logger.debug(f'{request.method} /warehouses/{id}')
    if request.method == 'GET':
        try:
            warehouse = models.Warehouse.query.get(id)
            if not warehouse:
                return jsonify({'error': 'Warehouse not found'}), 404

            warehouse_dto = schemas.WarehouseDto.from_orm(warehouse).dict()
            return jsonify({"warehouse": warehouse_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'PUT':
        try:
            warehouse = models.Warehouse.query.get(id)

            if not warehouse:
                return jsonify({'error': 'Warehouse not found'}), 404

            warehouse_dto = request.get_json()

            if 'quantity' in warehouse_dto:
                warehouse.quantity = warehouse_dto['quantity']
            if 'address' in warehouse_dto:
                warehouse.address = warehouse_dto['address']
            if 'product_id' in warehouse_dto:
                warehouse.product_id = warehouse_dto['product_id']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500

    if request.method == 'DELETE':
        try:
            warehouse = models.Warehouse.query.get(id)
            if warehouse:
                db.session.delete(warehouse)
                db.session.commit()

                return jsonify({'message': 'DELETED'}), 204
            else:
                return jsonify({'error': 'Warehouse not found'}), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
