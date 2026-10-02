from config.database import Database


def crear_tablas():
    db = Database()
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
        print("Tablas creadas correctamente.")
    finally:
        conexion.close()


if __name__ == "__main__":
    crear_tablas()
