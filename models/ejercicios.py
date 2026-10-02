import random


class Ejercicio:
    """Clase padre de los ejercicios."""

    def __init__(self, numero):
        self.numero = numero

    def resolver(self):
        raise NotImplementedError("Cada ejercicio debe implementar resolver().")


class EjercicioParImpar(Ejercicio):
    """Ejercicio 1."""

    def resolver(self):
        return "El número es par" if self.numero % 2 == 0 else "El número es impar"


class EjercicioMultiplicacion(Ejercicio):
    """Ejercicio 2."""

    def resolver(self):
        return [f"{self.numero} x {i} = {self.numero * i}" for i in range(1, 11)]

    def como_texto(self):
        return "\n".join(self.resolver())


class JuegoAdivina:
    """Ejercicio 3. Mantiene el estado del juego como un objeto."""

    def __init__(self, numero_secreto=None):
        self.numero_secreto = (
            numero_secreto if numero_secreto is not None else random.randint(1, 100)
        )

    def intentar(self, numero):
        if numero < self.numero_secreto:
            return "El número secreto es mayor"
        if numero > self.numero_secreto:
            return "El número secreto es menor"
        return "¡Correcto! Adivinaste el número"

    def acerto(self, numero):
        return numero == self.numero_secreto
