from http import HTTPStatus

from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from . import app, db
from .error_handlers import InvalidAPIUsage, NotFoundException
from .models import URLMap
from .validators import duplicate_validator, validator_custom_id
from .views import random_short_url


def create_new_object_api(data):
    try:
        short_url = URLMap()
        short_url.from_dict(data)
        db.session.add(short_url)
        db.session.commit()
        return short_url
    except SQLAlchemyError as e:
        db.session.rollback()
        raise InvalidAPIUsage(
            f'Ошибка при создании нового объекта URLMap: {e}'
        )


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not data.get('url'):
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if data.get('custom_id'):
        short = data.get('custom_id')
        validator_custom_id(data.get('custom_id'))
        duplicate_validator(short)
        short_url = create_new_object_api(data)
        return jsonify(short_url.to_dict()), HTTPStatus.CREATED
    short = random_short_url()
    duplicate_validator(short)
    data['custom_id'] = short
    short_url = create_new_object_api(data)
    return jsonify(short_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url:
        url = url.original
        return jsonify({'url': url}), HTTPStatus.OK
    raise NotFoundException('Указанный id не найден')
