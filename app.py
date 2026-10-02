from flask import Flask, render_template, request, session
from config.database import Database
from models.ejercicios import (
    EjercicioParImpar,
    EjercicioMultiplicacion,
    JuegoAdivina
)
from models.repositorios import (
    Ejercicio1Repositorio,
    Ejercicio2Repositorio,
    Ejercicio3Repositorio
)

app = Flask(__name__)
app.secret_key = "clave-secreta"

# Relaciones entre objetos:
# App -> Ejercicios -> Repositorios -> Database -> PostgreSQL
db = Database()
repo1 = Ejercicio1Repositorio(db)
repo2 = Ejercicio2Repositorio(db)
repo3 = Ejercicio3Repositorio(db)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = ""

    if request.method == "POST":
        numero = int(request.form["numero"])

        # Se crea un objeto de la clase EjercicioParImpar.
        ejercicio = EjercicioParImpar(numero)
        resultado = ejercicio.resolver()

        # El repositorio guarda el resultado en PostgreSQL.
        repo1.guardar(numero, resultado)

    return render_template("ejercicio1.html", resultado=resultado)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    tabla = []

    if request.method == "POST":
        numero = int(request.form["numero"])

        ejercicio = EjercicioMultiplicacion(numero)
        tabla = ejercicio.resolver()

        repo2.guardar(numero, ejercicio.como_texto())

    return render_template("ejercicio2.html", tabla=tabla)


@app.route("/ejercicio3", methods=["GET", "POST"])
def ejercicio3():
    resultado = ""

    if "juego" not in session:
        juego = JuegoAdivina()
        session["numero_secreto"] = juego.numero_secreto

    juego = JuegoAdivina(session["numero_secreto"])

    if request.method == "POST":
        numero = int(request.form["numero"])

        resultado = juego.intentar(numero)
        repo3.guardar(numero, juego.numero_secreto, resultado)

        if juego.acerto(numero):
            session.pop("numero_secreto", None)

    return render_template("ejercicio3.html", resultado=resultado)


if __name__ == "__main__":
    print("================================")
    print("CONECTANDO A POSTGRESQL")
    print("================================")

    try:
        db.probar_conexion()
        print("Conexión exitosa a PostgreSQL")
    except Exception as error:
        print("Error de conexión:")
        print(error)

    app.run(debug=True)
