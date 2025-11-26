# MyMLP.py
# Perceptron multicapa para clasificacion binaria 


# ----------------- Utilidades internas -----------------

# Potencia x^n para n entero
def _power(x, n):
    n = int(n)
    if n == 0:
        return 1.0
    if n < 0:
        return 1.0 / _power(x, -n)
    res = 1.0
    for _ in range(n):
        res *= x
    return res


def _factorial(n):
    n = int(n)
    if n < 0:
        raise ValueError("factorial indefinido para n < 0")
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


# Aproximacion de e^x usando serie de Taylor con pocos terminos 
def _exp(x):
    x = float(x)
    terms = 10
    res = 0.0
    for k in range(terms):
        res += _power(x, k) / _factorial(k)
    return res


# Funcion de activacion sigmoide
def _sigmoid(x):
    return 1.0 / (1.0 + _exp(-x))


# Derivada de la sigmoide en funcion del pre-activacion x
def _sigmoid_deriv(x):
    s = _sigmoid(x)
    return s * (1.0 - s)


# ----------------- Clase MLP -----------------
# Perceptron multicapa con:
#  - Capa de entrada: input_dim
#  - 1 capa oculta: hidden_dim
#  - Capa de salida: output_dim
# Activacion sigmoide en oculta y salida

class MLP:

    def __init__(self, input_dim, hidden_dim, output_dim):
        self.input_dim = int(input_dim)
        self.hidden_dim = int(hidden_dim)
        self.output_dim = int(output_dim)

        # Pesos capa 1: W1 (hidden_dim x input_dim)
        # Cada fila = pesos de una neurona oculta
        # Inicializacion determinista con signos alternados (sin random)
        self.W1 = []
        for h in range(self.hidden_dim):
            fila = []
            for i in range(self.input_dim):
                base = 0.1 * (h + 1 + i + 2)  # solo una formula cualquiera
                # alternar signos para romper simetria
                if (h + i) % 2 == 0:
                    base = -base
                fila.append(base)
            self.W1.append(fila)

        # Bias capa 1: b1 (hidden_dim)
        self.b1 = [0.0 for _ in range(self.hidden_dim)]

        # Pesos capa 2: W2 (output_dim x hidden_dim)
        # Cada fila = pesos de una neurona de salida
        self.W2 = []
        for o in range(self.output_dim):
            fila = []
            for h in range(self.hidden_dim):
                base = 0.1 * (o + 3 + h + 1)
                # alternar signos de forma distinta
                if (o + h) % 2 == 1:
                    base = -base
                fila.append(base)
            self.W2.append(fila)

        # Bias capa 2: b2 (output_dim)
        self.b2 = [0.0 for _ in range(self.output_dim)]

    # ----------------- Operaciones básicas con listas -----------------

    # Producto punto entre dos listas del mismo tamaño
    def _dot(self, a, b):
        if len(a) != len(b):
            raise ValueError("longitudes distintas en dot")
        s = 0.0
        for i in range(len(a)):
            s += a[i] * b[i]
        return s

    # Multiplicacion matriz por vector: M (filas) * v
    def _mat_vec(self, M, v):
        res = []
        for fila in M:
            res.append(self._dot(fila, v))
        return res

    # Suma elemento a elemento de vectores
    def _vec_add(self, a, b):
        if len(a) != len(b):
            raise ValueError("longitudes distintas en vec_add")
        res = []
        for i in range(len(a)):
            res.append(a[i] + b[i])
        return res

    # ----------------- Forward -----------------
    # Propagacion hacia adelante para un ejemplo x (lista de longitud input_dim)
    # Devuelve la salida (lista de longitud output_dim)

    def forward(self, x):
        if len(x) != self.input_dim:
            raise ValueError("dimension de entrada incorrecta")

        # capa oculta: z1 = W1 * x + b1
        z1 = self._mat_vec(self.W1, x)  # len = hidden_dim
        for i in range(self.hidden_dim):
            z1[i] += self.b1[i]
        h1 = [_sigmoid(z) for z in z1]

        # capa de salida: z2 = W2 * h1 + b2
        z2 = self._mat_vec(self.W2, h1)  # len = output_dim
        for j in range(self.output_dim):
            z2[j] += self.b2[j]
        out = [_sigmoid(z) for z in z2]

        # guardamos para backprop
        self.last_x = x
        self.last_z1 = z1
        self.last_h1 = h1
        self.last_z2 = z2
        self.last_out = out

        return out

    # ----------------- Entrenamiento -----------------
    # X: Lista de ejemplos, cada uno es lista de input_dim
    # Y: Lista de etiquetas. Para binario: 0 o 1
    # lr: learning rate
    # epochs: numero de pasadas por todo el dataset

    def train(self, X, Y, lr=0.1, epochs=1000):
        # se asegura que Y sea lista de listas si output_dim = 1
        Y_proc = []
        for y in Y:
            if self.output_dim == 1:
                Y_proc.append([float(y)])
            else:
                raise ValueError("Solo se ha implementado output_dim = 1")

        for _ in range(int(epochs)):
            for x, y in zip(X, Y_proc):
                # 1) forward
                out = self.forward(x)   # lista de tamaño output_dim

                # error en salida: error_j = out_j - y_j
                error_out = []
                for j in range(self.output_dim):
                    error_out.append(out[j] - y[j])

                # 2) gradientes capa de salida
                # dL/dz2_j = error_out_j * sig'(z2_j)
                d_z2 = []
                for j in range(self.output_dim):
                    d_z2.append(error_out[j] * _sigmoid_deriv(self.last_z2[j]))

                # gradientes para W2 y b2
                # W2: (output_dim x hidden_dim)
                # dL/dW2_jk = d_z2_j * h1_k
                for j in range(self.output_dim):
                    for k in range(self.hidden_dim):
                        grad = d_z2[j] * self.last_h1[k]
                        self.W2[j][k] -= lr * grad
                for j in range(self.output_dim):
                    self.b2[j] -= lr * d_z2[j]

                # 3) gradientes capa oculta
                # dL/dh1_k = sum_j d_z2_j * W2_jk
                d_h1 = []
                for k in range(self.hidden_dim):
                    s = 0.0
                    for j in range(self.output_dim):
                        s += d_z2[j] * self.W2[j][k]
                    d_h1.append(s)

                # dL/dz1_k = d_h1_k * sig'(z1_k)
                d_z1 = []
                for k in range(self.hidden_dim):
                    d_z1.append(d_h1[k] * _sigmoid_deriv(self.last_z1[k]))

                # gradientes para W1 y b1
                # W1: (hidden_dim x input_dim)
                # dL/dW1_ki = d_z1_k * x_i
                for k in range(self.hidden_dim):
                    for i in range(self.input_dim):
                        grad = d_z1[k] * self.last_x[i]
                        self.W1[k][i] -= lr * grad
                for k in range(self.hidden_dim):
                    self.b1[k] -= lr * d_z1[k]

    # ----------------- Prediccion -----------------

    # Predice una etiqueta 0/1 para un ejemplo x
    def predict_one(self, x):
        out = self.forward(x)[0]  # output_dim = 1
        return 1 if out >= 0.5 else 0

    # Para una lista de ejemplos X
    def predict(self, X):
        preds = []
        for x in X:
            preds.append(self.predict_one(x))
        return preds


# Prediccion numerica (regresion) con perceptron
# Devuelve los valores reales de salida sin convertir a binario
def predict_real_mlp(model, X):
    ys = []
    for x in X:
        out = model.forward(x)  # lista de tamaño output_dim
        if len(out) == 1:
            ys.append(out[0])
        else:
            ys.append(out)
    return ys


# ----------------- Funciones para el lenguaje -----------------

def create_mlp(input_dim, hidden_dim, output_dim):
    return MLP(input_dim, hidden_dim, output_dim)


def train_mlp(model, X, Y, lr, epochs):
    model.train(X, Y, lr, epochs)
    return model


def classify_mlp(model, X):
    return model.predict(X)


def predict_mlp(model, X):
    return model.predict(X)
