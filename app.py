import os

from flask import Flask, render_template, request, session
from config.database import Database
from config.crear_tablas import crear_tablas
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

AVISO_BD = (
    "El resultado es correcto, pero no se pudo guardar en PostgreSQL. "
    "Revisa que el servicio esté encendido y que la base de datos exista."
)


@app.context_processor
def version_css():
    """Cambia la URL del CSS cuando el archivo cambia, así el navegador
    nunca muestra una versión vieja guardada en caché."""
    ruta = os.path.join(app.static_folder, "style.css")
    return {"css_version": int(os.path.getmtime(ruta))}


def guardar_seguro(guardar, *datos):
    """Guarda en PostgreSQL. Si falla, la página sigue funcionando
    y devuelve un aviso en vez de mostrar un error 500."""
    try:
        guardar(*datos)
        return ""
    except Exception as error:
        print("Error al guardar en PostgreSQL:", error)
        return AVISO_BD


def leer_numero():
    """Devuelve el número del formulario o None si no es válido."""
    try:
        return int(request.form["numero"])
    except (KeyError, ValueError):
        return None


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = ""
    aviso = ""

    if request.method == "POST":
        numero = leer_numero()

        if numero is None:
            aviso = "Escribe un número entero válido."
        else:
            # Se crea un objeto de la clase EjercicioParImpar.
            ejercicio = EjercicioParImpar(numero)
            resultado = ejercicio.resolver()

            # El repositorio guarda el resultado en PostgreSQL.
            aviso = guardar_seguro(repo1.guardar, numero, resultado)

    return render_template("ejercicio1.html", resultado=resultado, aviso=aviso)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    tabla = []
    aviso = ""

    if request.method == "POST":
        numero = leer_numero()

        if numero is None:
            aviso = "Escribe un número entero válido."
        else:
            ejercicio = EjercicioMultiplicacion(numero)
            tabla = ejercicio.resolver()
            aviso = guardar_seguro(repo2.guardar, numero, ejercicio.como_texto())

    return render_template("ejercicio2.html", tabla=tabla, aviso=aviso)


@app.route("/ejercicio3", methods=["GET", "POST"])
def ejercicio3():
    resultado = ""
    aviso = ""
    acerto = False

    # El número secreto se crea una sola vez y se conserva en la sesión
    # hasta que el jugador acierta.
    if "numero_secreto" not in session:
        session["numero_secreto"] = JuegoAdivina().numero_secreto
        session["intentos"] = 0

    juego = JuegoAdivina(session["numero_secreto"])

    if request.method == "POST":
        numero = leer_numero()

        if numero is None:
            aviso = "Escribe un número entero válido."
        else:
            resultado = juego.intentar(numero)
            session["intentos"] = session.get("intentos", 0) + 1
            aviso = guardar_seguro(
                repo3.guardar, numero, juego.numero_secreto, resultado
            )

            if juego.acerto(numero):
                acerto = True
                session.pop("numero_secreto", None)

    intentos = session.get("intentos", 0)
    return render_template(
        "ejercicio3.html",
        resultado=resultado,
        aviso=aviso,
        acerto=acerto,
        intentos=intentos,
    )


if __name__ == "__main__":
    print("================================")
    print("CONECTANDO A POSTGRESQL")
    print("================================")

    # Solo se ejecuta en el proceso principal (debug=True lanza dos).
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        try:
            crear_tablas(db)
            print("Conexión exitosa a PostgreSQL (tablas listas)")
        except Exception as error:
            print("Error de conexión:")
            print(error)
            print("La página abrirá igual, pero no guardará datos.")

    app.run(debug=True)
