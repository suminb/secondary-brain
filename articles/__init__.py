import os

from flask import Flask


def create_app(name=__name__, config={}, static_folder='static',
               template_folder='templates'):
    app = Flask(name, static_folder=static_folder,
                template_folder=template_folder)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    app.config['DEBUG'] = True
    app.config.update(config)

    from articles.models import db
    db.init_app(app)

    return app
