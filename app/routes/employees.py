from flask import Blueprint, jsonify, request, render_template, flash
from sqlalchemy import select

from .. import db, logger
from .. import models
from .. import schemas

employees_bp = Blueprint('employees_bp', __name__)


@employees_bp.route('/employees', methods=['GET', 'POST'])
def employees():
    logger.debug(f'{request.method} /employees')

    if request.method == 'POST':
        try:
            employee = models.Employee(
                full_name=request.form.get('full_name'),
                post=request.form.get('post'),
                phone_number=request.form.get('phone_number'),
                email=request.form.get('email')
            )

            db.session.add(employee)
            db.session.commit()

            return jsonify({'message': 'CREATED'}), 201

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500

    try:
        query = (
            select(models.Employee)
        )
        employees = db.session.execute(query).scalars().all()
        employees_dto = [
            schemas.EmployeeDto.from_orm(employee).dict() for employee in employees
        ]

        return render_template('employees.html', employees=employees_dto), 200

    except Exception as ex:
        db.session.rollback()
        logger.exception(ex)
        return render_template('500.html'), 500


@employees_bp.route('/employees/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employee(id):
    logger.debug(f'{request.method} /employees/{id}')
    if request.method == 'GET':
        try:
            employee = models.Employee.query.get(id)
            if not employee:
                return render_template('404.html'), 404

            employee_dto = schemas.EmployeeDto.from_orm(employee).dict()
            return render_template('employee_card.html', empl=employee_dto), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500

    if request.method == 'PUT':
        try:
            employee = models.Employee.query.get(id)

            if not employee:
                return render_template('404.html'), 404

            employee_dto = request.get_json()

            if 'full_name' in employee_dto:
                employee.full_name = employee_dto['full_name']
            if 'post' in employee_dto:
                employee.post = employee_dto['post']
            if 'phone_number' in employee_dto:
                employee.phone_number = employee_dto['phone_number']
            if 'email' in employee_dto:
                employee.email = employee_dto['email']

            db.session.commit()

            return jsonify({'message': 'UPDATED'}), 200
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500

    if request.method == 'DELETE':
        try:
            employee = models.Employee.query.get(id)
            if employee:
                db.session.delete(employee)
                db.session.commit()
                flash('Сотрудник успешно удалён', 'success')
                return jsonify({'message': 'DELETED'}), 204
            else:
                return render_template('404.html'), 404
        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return render_template('500.html'), 500
