# MyClusterNN.py
# Red competitiva sencilla para AGRUPAMIENTO (clustering)

# Distancia euclidea al cuadrado entre dos vectores a y b
# No se usa sqrt porque no hace falta comparar distancies
def _squared_distance(a, b):
    if len(a) != len(b):
        raise ValueError("vectores de distinta longitud en _squared_distance")
    s = 0.0
    for i in range(len(a)):
        d = float(a[i]) - float(b[i])
        s += d * d
    return s


# Red competitiva:
# Input_dim: dimension de entrada
# num_clusters: numero de neuronas
class CompetitiveNet:

    def __init__(self, input_dim, num_clusters):
        self.input_dim = int(input_dim)
        self.num_clusters = int(num_clusters)

        # se inicializan centros de forma determinista
        # Por ejemplo, todos en 0.1*(i+1) para cada dimension.
        self.centers = []
        for j in range(self.num_clusters):
            c = []
            base = 0.1 * (j + 1)
            for _ in range(self.input_dim):
                c.append(base)
            self.centers.append(c)
            
    # Devuelve el indice del centro mas cercano a x
    def _winner(self, x):
        best_j = 0
        best_d = _squared_distance(x, self.centers[0])
        for j in range(1, self.num_clusters):
            d = _squared_distance(x, self.centers[j])
            if d < best_d:
                best_d = d
                best_j = j
        return best_j

    # Entrenamiento no supervisado:
    # X: lista de ejmplos
    # lr: tasa de aprendizaje
    # epcochs: numero de pasadas por todos los datos
    def train(self, X, lr=0.1, epochs=10):
        lr = float(lr)
        for _ in range(int(epochs)):
            for x in X:
                # aseguramos floats
                xv = [float(v) for v in x]
                j = self._winner(xv)

                # se actualiza solo el centro j 
                for i in range(self.input_dim):
                    self.centers[j][i] += lr * (xv[i] - self.centers[j][i])
                    
    # Devuelve el indice del cluster ganador para un ejemplo x
    def predict_one(self, x):
        xv = [float(v) for v in x]
        return self._winner(xv)

    # Devuelve la lista de indices de cluster para cada ejemplo en X
    def predict(self, X):
        labels = []
        for x in X:
            labels.append(self.predict_one(x))
        return labels


# Funciones para el lenguaje

# Crea y devuelve una red competitiva para clustering
def create_cluster_net(input_dim, num_clusters):
    return CompetitiveNet(input_dim, num_clusters)

# Entrena la red competitiva con los datos X
def train_cluster_net(model, X, lr, epochs):
    model.train(X, lr, epochs)
    return model

# Devuelve los indices de cluster para cada ejemplo en X
def predict_cluster(model, X):
    return model.predict(X)
