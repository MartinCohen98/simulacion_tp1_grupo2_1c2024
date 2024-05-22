import numpy as np

# Parámetros definidos en el paper
MATRIX_SIZE = 139  # Tamaño del vector y la matriz
MAGIC_NUMBER = -1  # Magic number
MAGIC_MODULUS = 9223372036853751941  # Modulus


class MixmaxRNG:

    def __init__(self, seed, size=MATRIX_SIZE, magic_number=MAGIC_NUMBER, period=MAGIC_MODULUS):
        # crea la matriz
        self.matrix = self._generate_mixmax_matrix(size, magic_number)
        # crea el vector inicial (no se retornarán sus valores)
        self.vector = self._generate_initial_vector(seed, size, period)

    """generates a uniform pseudo random value between 0 and 1,
    you can add an interval (a, b) to return a value between a and b"""

    def generate_number(self, interval=(0, 1)):
        # valor pseudo aleatorio
        result = self._generate_new_vector()[0]
        return self._to_interval(result, interval)

    """calculates a new vector of numbers and replaces the current one with the new one with mod 1"""

    def _generate_new_vector(self):
        # calculo el nuevo vector
        new_vector = np.matmul(self.matrix, self.vector)
        # actualizo el vector con mod 1
        self.vector = [i % 1 for i in new_vector]
        return self.vector

    def _to_interval(self, number, interval):
        # encuentro la escala para multiplicar el valor
        scale = interval[1] - interval[0]
        # retorno el valor por la escala trasladando el 0 al minimo del intervalo
        return (number * scale) + interval[0]

    @staticmethod
    def _generate_initial_vector(seed, size, period):
        # Multiplicador
        a = 6364136223846793005
        # Incremento
        c = 1
        # Vector a ser utilizado como semilla
        random_numbers = []
        # Semilla para generar las componentes del vector
        x = seed
        # Calculamos cada componente del vector inicial
        for _ in range(size):
            x = ((a * x + c) % period) / period
            random_numbers.append(x)
        return random_numbers

    @staticmethod
    def _generate_mixmax_matrix(size, magic_number):
        # Inicializamos la matrix MIXMAX con 1's
        matrix = np.ones((size, size), dtype=int)
        # Completamos los valores de la matriz con el patrón especificado
        for i in range(size):
            for j in range(size):
                if i == j and j > 0:
                    matrix[i][j] = 2
                elif j < i and j > 0:
                    matrix[i][j] = (i + 1) - (j - 1)
        matrix[2][1] += magic_number
        return matrix
