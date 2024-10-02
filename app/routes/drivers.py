from flask import Blueprint, abort, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from .. import db, logger
from .. import models
from .. import schemas
from ..models import Driver
from ..services.check_post import admin_required
from ..services.drivers import DriverService

drivers_bp = Blueprint('drivers_bp', __name__)


@drivers_bp.route('/drivers', methods=['GET', 'POST'])
@login_required
@admin_required
def drivers():
    logger.debug(f'{request.method} /drivers')

    if request.method == 'POST':
        try:
            driver = models.Driver(
                full_name=request.form.get('full_name'),
                phone_number=request.form.get('phone_number'),
                car_type=request.form.get('car_type')
            )

            db.session.add(driver)
            db.session.commit()

            flash('Водитель добавлен успешно', 'success')
            return redirect(url_for('drivers_bp.drivers'))

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            return redirect(url_for('drivers_bp.drivers'))

    try:
        return render_template('drivers.html', drivers=DriverService.get_drivers()), 200
    except SQLAlchemyError as ex:
        db.session.rollback()
        logger.exception(ex)
        abort(500)


@drivers_bp.route('/drivers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
@admin_required
def driver(id):
    logger.debug(f'{request.method} /drivers/{id}')
    if request.method == 'GET':
        try:
            driver = models.Driver.query.get(id)
            if not driver:
                abort(404)

            driver_dto = schemas.DriverDto.from_orm(driver).dict()

            return render_template('driver_card.html', driver=driver_dto), 200

        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'PUT':
        try:
            driver = models.Driver.query.get(id)

            if not driver:
                abort(404)

            driver_dto = request.get_json()

            if 'full_name' in driver_dto:
                driver.full_name = driver_dto['full_name']
            if 'phone_number' in driver_dto:
                driver.phone_number = driver_dto['phone_number']
            if 'car_type' in driver_dto:
                driver.car_type = driver_dto['car_type']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)

    if request.method == 'DELETE':
        try:
            driver = models.Driver.query.get(id)
            if driver:
                db.session.delete(driver)
                db.session.commit()
                flash('Водитель успешно удалён', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                abort(404)
        except SQLAlchemyError as ex:
            db.session.rollback()
            logger.exception(ex)
            abort(500)


@drivers_bp.route('/search/drivers/', methods=['GET'])
@login_required
@admin_required
def search():
    logger.debug(f'{request.method} /search/drivers/')

    full_name = request.args.get('full_name')
    phone_number = request.args.get('phone_number')
    car_type = request.args.get('car_type')

    query = Driver.query

    if full_name:
        query = query.filter(Driver.full_name == full_name)
    if phone_number:
        query = query.filter(Driver.phone_number == phone_number)
    if car_type:
        query = query.filter(Driver.car_type == car_type)

    try:
        filter_drivers = query.all()
        return render_template('found_drivers.html', drivers=filter_drivers), 200

    except SQLAlchemyError as ex:
        logger.exception(ex)
        abort(500)
