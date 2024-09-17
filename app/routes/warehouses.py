from flask import Blueprint, abort, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from .. import db, logger
from .. import models
from .. import schemas

warehouses_bp = Blueprint('warehouses_bp', __name__)


@warehouses_bp.route('/warehouses', methods=['GET', 'POST'])
@login_required
def warehouses():
    logger.debug(f'{request.method} /warehouses')

    if request.method == 'POST':
        try:
            warehouse = models.Warehouse(
                quantity=request.form.get('quantity'),
                address=request.form.get('address'),
                product_id=request.form.get('product_id')
            )

            db.session.add(warehouse)
            db.session.commit()

            flash('Склад добавлен успешно', 'success')
            return redirect(url_for('warehouses_bp.warehouses'))

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)
    try:
        query = (
            select(models.Warehouse)
        )
        warehouses = db.session.execute(query).scalars().all()
        warehouses_dto = [
            schemas.WarehouseDto.from_orm(warehouse).dict() for warehouse in warehouses
        ]

        return render_template('warehouses.html', warehouses=warehouses_dto), 200

    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@warehouses_bp.route('/warehouses/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def warehouse(id):
    logger.debug(f'{request.method} /warehouses/{id}')
    if request.method == 'GET':
        try:
            warehouse = models.Warehouse.query.get(id)
            if not warehouse:
                abort(404)

            warehouse_dto = schemas.WarehouseDto.from_orm(warehouse).dict()
            return render_template('warehouse_card.html', w=warehouse_dto), 200

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'PUT':
        try:
            warehouse = models.Warehouse.query.get(id)

            if not warehouse:
                abort(404)

            warehouse_dto = request.get_json()

            if 'quantity' in warehouse_dto:
                warehouse.quantity = warehouse_dto['quantity']
            if 'address' in warehouse_dto:
                warehouse.address = warehouse_dto['address']
            if 'product_id' in warehouse_dto:
                warehouse.product_id = warehouse_dto['product_id']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'DELETE':
        try:
            warehouse = models.Warehouse.query.get(id)
            if warehouse:
                db.session.delete(warehouse)
                db.session.commit()

                flash('Склад успешно удалён', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                abort(404)
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)
