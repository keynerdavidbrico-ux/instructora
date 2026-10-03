import os
import sys

# Permite ejecutar este archivo directamente (python config/crear_tablas.py)
# sin el error "No module named 'config'".
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import Database


def crear_tablas(db=None):
    db = db or Database()
    conexion = db.conectar()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ejercicio1 (
                    id SERIAL PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    resultado VARCHAR(20) NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ejercicio2 (
                    id SERIAL PRIMARY KEY,
                    numero INTEGER NOT NULL,
                    resultado TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ejercicio3 (
                    id SERIAL PRIMARY KEY,
                    intento INTEGER NOT NULL,
                    numero_secreto INTEGER NOT NULL,
                    resultado VARCHAR(50) NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

        conexion.commit()
    finally:
        conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas correctamente.")
