# Ejercicios Python con POO

Proyecto con Flask, PostgreSQL y programación orientada a objetos.

## Estructura

- `app.py`: rutas y coordinación de objetos.
- `config/database.py`: clase `Database`, encargada de PostgreSQL.
- `models/ejercicios.py`: clases de los ejercicios.
- `models/repositorios.py`: clases que guardan los datos.
- `templates/`: interfaz HTML (`base.html` es la plantilla común).
- `static/style.css`: diseño visual.

## Relaciones orientadas a objetos

- `EjercicioParImpar` y `EjercicioMultiplicacion` **heredan** de `Ejercicio`.
- `Repositorio` es la clase base de los repositorios.
- Cada repositorio **tiene una relación de composición/asociación** con `Database`.
- `app.py` crea y utiliza objetos de los ejercicios y repositorios.
- Los repositorios utilizan `Database` para comunicarse con PostgreSQL.

## Ejecutar

1. Activar el entorno virtual.
2. Instalar `flask` y `psycopg2`.
3. Crear la base de datos `Ejercicios`.
4. Ejecutar `python app.py` (crea las tablas solas si no existen; también puedes usar `python config/crear_tablas.py`).
5. Abrir `http://127.0.0.1:5000` en el navegador. No abras los `.html` con doble clic: necesitan Flask para mostrar el diseño.
