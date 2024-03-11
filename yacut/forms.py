from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        default=None,
        validators=[
            Length(
                1, 16, message='Длина поля должна быть от 1 до 16 символов'
            ),
            Optional(),
            Regexp(
                '^[a-zA-Z0-9]*$',
                message='Можно использовать только латинские буквы и цифры.',
            ),
        ],
    )
    submit = SubmitField('Создать')
