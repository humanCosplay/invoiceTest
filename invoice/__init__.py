from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import STATIC_DIR, TEMPLATE_DIR

db = SQLAlchemy()


def create_app(configClass='config.DevelopmentConfiguration'):
    app = Flask(__name__, static_url_path='/static', 
                            static_folder=STATIC_DIR,
                             template_folder=TEMPLATE_DIR)

    app.config.from_object(configClass)
    db.init_app(app)

    from invoice.main.routes import main
    app.register_blueprint(main)

    return app