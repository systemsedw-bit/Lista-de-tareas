import os
from flask import Flask

from .database import init_app, init_db


def create_app(test_config=None):
    """Crea y configura la aplicación Flask.

    Esta función permite ejecutar la app en modo normal y también facilita
    las pruebas unitarias con una base de datos temporal.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-key-lista-tareas"),
        DATABASE=os.path.join(app.instance_path, "tareas.sqlite"),
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    init_app(app)

    with app.app_context():
        init_db()

    from .routes import bp

    app.register_blueprint(bp)
    app.add_url_rule("/", endpoint="index")

    return app
