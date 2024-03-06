from flask import request, jsonify

from .models import URLMap
from . import app, db
from .error_handlers import InvalidAPIUsage
from .views import random_short_url
from sqlalchemy.exc import SQLAlchemyError
from .validators import validator_custom_id, duplicate_validator


def create_new_object_api(data):
    try:
        short_url = URLMap()
        short_url.from_dict(data)
        db.session.add(short_url)
        db.session.commit()
        return short_url
    except SQLAlchemyError as e:
        db.session.rollback()
        raise InvalidAPIUsage(f"Ошибка при создании нового объекта URLMap: {e}")
    

@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if data.get('url') is None or data.get('url') == '':
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'custom_id' in data:
        short = data.get('custom_id')
        validator_custom_id(data.get('custom_id'))
        duplicate_validator(short)
        short_url = create_new_object_api(data)
        return jsonify(short_url.to_dict()), 201
    else:
        short = random_short_url()
        duplicate_validator(short)
        data['custom_id'] = short
        short_url = create_new_object_api(data)
        return jsonify(short_url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url:
        url = url.original
        return jsonify({"url": url}), 200
    else:
        raise InvalidAPIUsage('Указанный id не найден', 404)