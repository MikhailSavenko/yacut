from .error_handlers import InvalidAPIUsage
import re
from .models import URLMap


def validator_custom_id(custom_id):
    if not (1 <= len(custom_id) <= 16):
        raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки")

    if not re.match("^[a-zA-Z0-9]+$", custom_id):
        raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки")


def duplicate_validator(short):
    if URLMap.query.filter_by(short=short).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
