from flask import Blueprint, jsonify, request

from .. import db, logger
from .. import models
from .. import schemas

managers_bp = Blueprint('managers_bp', __name__)


@managers_bp.route('/managers/<int:id>', methods=['GET'])
def profile(id):
    logger.debug(f'{request.method} /managers/{id}')
    if request.method == 'GET':
        try:
            manager = models.Employee.query.get(id)
            if not manager:
                return jsonify({'error': 'Manager not found'}), 404

            if manager.post.lower() != 'менеджер' and manager.post.lower() != 'manager':
                return jsonify({'error': 'Forbidden'}), 403

            manager_dto = schemas.ManagerDto.from_orm(manager).dict()

            return jsonify({"manager": manager_dto}), 200

        except Exception as ex:
            db.session.rollback()
            logger.exception(ex)
            return jsonify({'error': 'Internal Server Error', 'message': str(ex)}), 500
