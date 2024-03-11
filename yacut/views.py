import logging
import random
import string
from http import HTTPStatus

from flask import Markup, abort, flash, redirect, render_template, url_for
from sqlalchemy.exc import SQLAlchemyError

from . import app, db
from .forms import UrlForm
from .models import URLMap


def create_new_object(original, short) -> object:
    try:
        short_url = URLMap(original=original, short=short)
        db.session.add(short_url)
        db.session.commit()
        return short_url
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f'Ошибка при создании нового объекта URLMap: {e}')


def random_short_url(length=6) -> str:
    characters = string.ascii_letters + string.digits
    short = ''.join(random.choices(characters, k=length))
    return short


def get_short(form, original, short):
    if URLMap.query.filter_by(short=short).first():
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html', form=form)
    short_url = create_new_object(original=original, short=short)
    short = url_for('get_website', short=f'{short_url.short}', _external=True)
    flash(
        Markup(
            f'Ваша новая ссылка готова: <br> <a href="{short}" target="_blank">{short}</a>'
        )
    )
    return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    original = form.original_link.data
    if short:
        get_short(form, original, short)
        return render_template('index.html', form=form)
    short = random_short_url()
    get_short(form, original, short)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def get_website(short):
    url_website = URLMap.query.filter_by(short=short).first()
    if url_website:
        return redirect(url_website.original)
    else:
        abort(HTTPStatus.NOT_FOUND)
