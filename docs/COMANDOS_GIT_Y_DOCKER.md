# Comandos de entrega: Git, pruebas y Docker

## 1. Crear repositorio local y primer commit

```bash
git init
git add .
git commit -m "Implementación inicial de la app Lista de Tareas"
```

## 2. Crear y publicar rama main

```bash
git branch -M main
git remote add origin https://github.com/USUARIO/Lista-de-tareas.git
git push -u origin main
```

## 3. Crear rama develop

```bash
git checkout -b develop
git push -u origin develop
```

## 4. Ejecutar pruebas unitarias

```bash
pytest
```

## 5. Ejecutar con Docker

```bash
docker build -t lista-tareas-flask .
docker run -p 5000:5000 lista-tareas-flask
```

Abrir en el navegador:

```text
http://localhost:5000
```
