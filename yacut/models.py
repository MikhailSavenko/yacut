from datetime import datetime

from flask import url_for
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        short = url_for('get_website', short=self.short, _external=True)
        return dict(url=self.original, short_link=short)

    def from_dict(self, data):
        if 'url' in data:
            self.original = data['url']
        if 'custom_id' in data:
            self.short = data['custom_id']
