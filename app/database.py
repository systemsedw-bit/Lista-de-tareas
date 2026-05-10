import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    """Retorna una conexión SQLite reutilizable durante la petición."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Cierra la conexión con la base de datos al finalizar la petición."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def _ensure_columns(db):
    """Agrega columnas nuevas si el usuario ejecuta la app sobre una BD anterior."""
    existing = {row["name"] for row in db.execute("PRAGMA table_info(tareas)").fetchall()}
    migrations = {
        "categoria": "ALTER TABLE tareas ADD COLUMN categoria TEXT NOT NULL DEFAULT 'Universidad'",
        "fecha_limite": "ALTER TABLE tareas ADD COLUMN fecha_limite TEXT DEFAULT ''",
    }

    for column, statement in migrations.items():
        if column not in existing:
            db.execute(statement)


def init_db():
    """Inicializa la base de datos con el esquema del proyecto."""
    db = get_db()
    schema_path = Path(__file__).with_name("schema.sql")
    with schema_path.open("r", encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())
    _ensure_columns(db)
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
