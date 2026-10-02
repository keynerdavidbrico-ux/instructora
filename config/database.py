import psycopg2


class Database:
    """Encapsula la conexión y operaciones básicas con PostgreSQL."""

    def __init__(self):
        self.host = "localhost"
        self.port = "5432"
        self.database = "Ejercicios"
        self.user = "postgres"
        self.password = "sebas2006"

    def conectar(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def ejecutar(self, consulta, parametros=()):
        conexion = self.conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, parametros)
            conexion.commit()
        finally:
            conexion.close()

    def probar_conexion(self):
        conexion = self.conectar()
        conexion.close()
        return True
