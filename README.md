# Lista de Tareas - Dashboard Profesional

Aplicación web básica desarrollada con Python y Flask para registrar, editar, completar y eliminar tareas. La interfaz fue mejorada con un dashboard profesional que separa actividades en tres listas principales: Universidad, Casa y Trabajo.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- pytest
- Git/GitHub
- Docker

## Estructura del proyecto

```text
Lista-de-tareas/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── routes.py
│   ├── schema.sql
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── editar.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── tests/
│   └── test_app.py
├── Dockerfile
├── requirements.txt
├── run.py
├── .gitignore
└── README.md
```

## Funcionalidades

- Dashboard general con total, pendientes, completadas y tareas de alta prioridad.
- Listas separadas para Universidad, Casa y Trabajo.
- Registro de tareas con categoría, prioridad, fecha límite y descripción.
- Filtros por estado, categoría y búsqueda por texto.
- Edición de tareas.
- Cambio de estado entre pendiente y completada.
- Eliminación con confirmación interactiva.
- Pruebas unitarias con pytest.
- Dockerfile funcional.

## Ejecución local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Ejecutar pruebas

```bash
pytest
```

## Ejecutar con Docker

Construir imagen:

```bash
docker build -t lista-tareas-flask .
```

Ejecutar contenedor:

```bash
docker run -p 5000:5000 lista-tareas-flask
```

Abrir:

```text
http://localhost:5000
```

## Flujo Git sugerido

```bash
git init
git add .
git commit -m "Mejora de interfaz con dashboard profesional"
git branch -M main
git checkout -b develop
git push -u origin main
git push -u origin develop
```
