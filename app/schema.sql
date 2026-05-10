CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT DEFAULT '',
    categoria TEXT NOT NULL DEFAULT 'Universidad',
    prioridad TEXT NOT NULL DEFAULT 'Media',
    estado TEXT NOT NULL DEFAULT 'Pendiente',
    fecha_limite TEXT DEFAULT '',
    fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
