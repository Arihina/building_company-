from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from sqlalchemy import select

from .. import db, logger
from .. import models
from .. import schemas

consists_bp = Blueprint('consists_bp', __name__)


@consists_bp.route('/consists', methods=['GET', 'POST'])
def consists():
    logger.debug(f'{request.method} /consists')

    if request.method == 'POST':
        try:
            consist = models.Consist(
                data=request.form.get('data'),
                order_amount=request.form.get('order_amount'),
                account_number=request.form.get('account_number'),
                product_id=request.form.get('product_id')
            )

            db.session.add(consist)
            db.session.commit()

            flash('Содержание добавлено успешно', 'success')
            return redirect(url_for('consists_bp.consists'))

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            flash('Произошла ошибка.', 'error')
            return render_template('500.html'), 500

    try:
        query = (
            select(models.Consist)
        )
        consists = db.session.execute(query).scalars().all()
        consists_dto = [
            schemas.ConsistDto.from_orm(consist).dict() for consist in consists
        ]

        return render_template('consists.html', consists=consists_dto), 200

    except Exception as ex:
        db.session.rollback()
        logger.exception(ex)
        return render_template('500.html'), 500


@consists_bp.route('/consists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def consist(id):
    logger.debug(f'{request.method} /consists/{id}')
    if request.method == 'GET':
        try:
            consist = models.Consist.query.get(id)
            if not consist:
                return render_template('404.html'), 404

            consist_dto = schemas.ConsistDto.from_orm(consist).dict()
            return render_template('consist_card.html', cons=consist_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500

    if request.method == 'PUT':
        try:
            consist = models.Consist.query.get(id)

            if not consist:
                return render_template('404.html'), 404

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
            return render_template('500.html'), 500

    if request.method == 'DELETE':
        try:
            consist = models.Consist.query.get(id)
            if consist:
                db.session.delete(consist)
                db.session.commit()

                flash('Содержание успешно удалено', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                return render_template('404.html'), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500
