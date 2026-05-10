from flask import Blueprint, flash, redirect, render_template, request, url_for

from .database import get_db

bp = Blueprint("tareas", __name__)

CATEGORIAS = ("Universidad", "Casa", "Trabajo")
PRIORIDADES = ("Alta", "Media", "Baja")
ESTADOS = ("Todas", "Pendiente", "Completada")


def _normalizar_categoria(valor):
    return valor if valor in CATEGORIAS else "Universidad"


def _normalizar_prioridad(valor):
    return valor if valor in PRIORIDADES else "Media"


def _calcular_porcentaje(completadas, total):
    if total == 0:
        return 0
    return round((completadas / total) * 100)


@bp.route("/", methods=["GET"])
def index():
    """Muestra el dashboard principal de tareas por universidad, casa y trabajo."""
    db = get_db()
    filtro_estado = request.args.get("estado", "Todas")
    filtro_categoria = request.args.get("categoria", "Todas")
    busqueda = request.args.get("q", "").strip()

    if filtro_estado not in ESTADOS:
        filtro_estado = "Todas"
    if filtro_categoria not in (*CATEGORIAS, "Todas"):
        filtro_categoria = "Todas"

    condiciones = []
    parametros = []

    if filtro_estado in ("Pendiente", "Completada"):
        condiciones.append("estado = ?")
        parametros.append(filtro_estado)

    if filtro_categoria in CATEGORIAS:
        condiciones.append("categoria = ?")
        parametros.append(filtro_categoria)

    if busqueda:
        condiciones.append("(titulo LIKE ? OR descripcion LIKE ?)")
        parametros.extend([f"%{busqueda}%", f"%{busqueda}%"])

    consulta = "SELECT * FROM tareas"
    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    consulta += " ORDER BY CASE prioridad WHEN 'Alta' THEN 1 WHEN 'Media' THEN 2 ELSE 3 END, id DESC"

    tareas = db.execute(consulta, parametros).fetchall()

    total = db.execute("SELECT COUNT(*) AS total FROM tareas").fetchone()["total"]
    pendientes = db.execute(
        "SELECT COUNT(*) AS total FROM tareas WHERE estado = 'Pendiente'"
    ).fetchone()["total"]
    completadas = db.execute(
        "SELECT COUNT(*) AS total FROM tareas WHERE estado = 'Completada'"
    ).fetchone()["total"]
    alta_prioridad = db.execute(
        "SELECT COUNT(*) AS total FROM tareas WHERE prioridad = 'Alta' AND estado = 'Pendiente'"
    ).fetchone()["total"]

    resumen_categorias = []
    for categoria in CATEGORIAS:
        total_cat = db.execute(
            "SELECT COUNT(*) AS total FROM tareas WHERE categoria = ?", (categoria,)
        ).fetchone()["total"]
        pendientes_cat = db.execute(
            "SELECT COUNT(*) AS total FROM tareas WHERE categoria = ? AND estado = 'Pendiente'",
            (categoria,),
        ).fetchone()["total"]
        completadas_cat = db.execute(
            "SELECT COUNT(*) AS total FROM tareas WHERE categoria = ? AND estado = 'Completada'",
            (categoria,),
        ).fetchone()["total"]
        resumen_categorias.append(
            {
                "nombre": categoria,
                "total": total_cat,
                "pendientes": pendientes_cat,
                "completadas": completadas_cat,
                "progreso": _calcular_porcentaje(completadas_cat, total_cat),
            }
        )

    tareas_por_categoria = {
        categoria: [tarea for tarea in tareas if tarea["categoria"] == categoria]
        for categoria in CATEGORIAS
    }

    return render_template(
        "index.html",
        tareas=tareas,
        tareas_por_categoria=tareas_por_categoria,
        categorias=CATEGORIAS,
        prioridades=PRIORIDADES,
        filtro_estado=filtro_estado,
        filtro_categoria=filtro_categoria,
        busqueda=busqueda,
        total=total,
        pendientes=pendientes,
        completadas=completadas,
        alta_prioridad=alta_prioridad,
        progreso_general=_calcular_porcentaje(completadas, total),
        resumen_categorias=resumen_categorias,
    )


@bp.route("/agregar", methods=["POST"])
def agregar():
    """Registra una nueva tarea desde el formulario."""
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    categoria = _normalizar_categoria(request.form.get("categoria", "Universidad"))
    prioridad = _normalizar_prioridad(request.form.get("prioridad", "Media"))
    fecha_limite = request.form.get("fecha_limite", "").strip()

    if not titulo:
        flash("El título de la tarea es obligatorio.", "error")
        return redirect(url_for("index"))

    db = get_db()
    db.execute(
        """
        INSERT INTO tareas (titulo, descripcion, categoria, prioridad, estado, fecha_limite)
        VALUES (?, ?, ?, ?, 'Pendiente', ?)
        """,
        (titulo, descripcion, categoria, prioridad, fecha_limite),
    )
    db.commit()
    flash(f"Tarea registrada correctamente en {categoria}.", "success")
    return redirect(url_for("index", categoria=categoria))


@bp.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id):
    """Cambia el estado de una tarea entre pendiente y completada."""
    db = get_db()
    tarea = db.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()

    if tarea is None:
        flash("La tarea seleccionada no existe.", "error")
        return redirect(url_for("index"))

    nuevo_estado = "Completada" if tarea["estado"] == "Pendiente" else "Pendiente"
    db.execute("UPDATE tareas SET estado = ? WHERE id = ?", (nuevo_estado, tarea_id))
    db.commit()
    flash("Estado de la tarea actualizado.", "success")
    return redirect(url_for("index", categoria=tarea["categoria"]))


@bp.route("/editar/<int:tarea_id>", methods=["GET", "POST"])
def editar(tarea_id):
    """Permite editar el contenido de una tarea."""
    db = get_db()
    tarea = db.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()

    if tarea is None:
        flash("La tarea seleccionada no existe.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = _normalizar_categoria(request.form.get("categoria", tarea["categoria"]))
        prioridad = _normalizar_prioridad(request.form.get("prioridad", tarea["prioridad"]))
        fecha_limite = request.form.get("fecha_limite", "").strip()

        if not titulo:
            flash("El título de la tarea es obligatorio.", "error")
            return render_template(
                "editar.html",
                tarea=tarea,
                categorias=CATEGORIAS,
                prioridades=PRIORIDADES,
            )

        db.execute(
            """
            UPDATE tareas
            SET titulo = ?, descripcion = ?, categoria = ?, prioridad = ?, fecha_limite = ?
            WHERE id = ?
            """,
            (titulo, descripcion, categoria, prioridad, fecha_limite, tarea_id),
        )
        db.commit()
        flash("Tarea actualizada correctamente.", "success")
        return redirect(url_for("index", categoria=categoria))

    return render_template(
        "editar.html",
        tarea=tarea,
        categorias=CATEGORIAS,
        prioridades=PRIORIDADES,
    )


@bp.route("/eliminar/<int:tarea_id>", methods=["POST"])
def eliminar(tarea_id):
    """Elimina una tarea por su identificador."""
    db = get_db()
    tarea = db.execute("SELECT categoria FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
    categoria = tarea["categoria"] if tarea else "Todas"
    db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
    db.commit()
    flash("Tarea eliminada correctamente.", "success")
    return redirect(url_for("index", categoria=categoria))
