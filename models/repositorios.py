from config.database import Database


class Repositorio:
    """Clase base para centralizar el acceso a PostgreSQL."""

    def __init__(self, db=None):
        self.db = db or Database()


class Ejercicio1Repositorio(Repositorio):
    def guardar(self, numero, resultado):
        self.db.ejecutar(
            """
            INSERT INTO ejercicio1 (numero, resultado)
            VALUES (%s, %s)
            """,
            (numero, resultado)
        )


class Ejercicio2Repositorio(Repositorio):
    def guardar(self, numero, resultado):
        self.db.ejecutar(
            """
            INSERT INTO ejercicio2 (numero, resultado)
            VALUES (%s, %s)
            """,
            (numero, resultado)
        )


class Ejercicio3Repositorio(Repositorio):
    def guardar(self, intento, secreto, resultado):
        self.db.ejecutar(
            """
            INSERT INTO ejercicio3 (intento, numero_secreto, resultado)
            VALUES (%s, %s, %s)
            """,
            (intento, secreto, resultado)
        )
