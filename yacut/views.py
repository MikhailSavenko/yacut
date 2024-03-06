from .models import URLMap
from . import app, db
from flask import render_template, flash, Markup, redirect, abort
from .forms import UrlForm
import random
import string
from sqlalchemy.exc import SQLAlchemyError


def create_new_object(original, short) -> object:
    try:
        short_url = URLMap(original=original, short=short)
        db.session.add(short_url)
        db.session.commit()
        return short_url
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Ошибка при создании нового объекта URLMap: {e}")


def random_short_url(length=6) -> str:
    characters = string.ascii_letters + string.digits
    short = ''.join(random.choices(characters, k=length))
    return short


def get_short(form, original, short):
    if URLMap.query.filter_by(short=short).first():
        flash('Предложенный вариант короткой ссылки уже существует.')
        return render_template('index.html', form=form)
    short_url = create_new_object(original=original, short=short)
    short = 'http://localhost/' + short_url.short
    flash(
        Markup(
            f'Ваша новая ссылка готова: <br> <a href="{short}" target="_blank">{short}</a>'
        )
    )
    return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        original = form.original_link.data
        if short:
            get_short(form, original, short)
            return render_template('index.html', form=form)
        else:
            short = random_short_url()
            get_short(form, original, short)
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def get_website(short):
    url_website = URLMap.query.filter_by(short=short).first()
    if url_website:
        return redirect(url_website.original)
    else:
        abort(404)
