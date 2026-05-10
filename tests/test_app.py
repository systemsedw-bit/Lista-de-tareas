import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "test_tareas.sqlite"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(database_path),
            "SECRET_KEY": "test-key",
        }
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_dashboard_principal_carga_correctamente(client):
    """Objetivo: validar que el dashboard principal responda sin errores."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Lista de Tareas" in response.data
    assert b"Universidad" in response.data
    assert b"Casa" in response.data
    assert b"Trabajo" in response.data


def test_agregar_tarea_universidad(client):
    """Objetivo: verificar que una tarea universitaria pueda registrarse desde el formulario."""
    response = client.post(
        "/agregar",
        data={
            "titulo": "Estudiar pruebas unitarias",
            "descripcion": "Preparar evidencia para la evaluacion final",
            "categoria": "Universidad",
            "prioridad": "Alta",
            "fecha_limite": "2026-05-10",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Estudiar pruebas unitarias" in response.data
    assert b"Universidad" in response.data
    assert b"Tarea registrada correctamente" in response.data


def test_agregar_tarea_casa_y_filtrar_categoria(client):
    """Objetivo: validar el filtro de lista Casa."""
    client.post(
        "/agregar",
        data={
            "titulo": "Ordenar escritorio",
            "descripcion": "Preparar el espacio de estudio",
            "categoria": "Casa",
            "prioridad": "Media",
        },
        follow_redirects=True,
    )

    response = client.get("/?categoria=Casa")

    assert response.status_code == 200
    assert b"Ordenar escritorio" in response.data
    assert b"Casa" in response.data


def test_completar_tarea(client):
    """Objetivo: comprobar el cambio de estado de una tarea registrada."""
    client.post(
        "/agregar",
        data={
            "titulo": "Subir proyecto a GitHub",
            "descripcion": "Usar ramas main y develop",
            "categoria": "Trabajo",
            "prioridad": "Media",
        },
        follow_redirects=True,
    )

    response = client.post("/completar/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"Completada" in response.data
    assert b"Estado de la tarea actualizado" in response.data
