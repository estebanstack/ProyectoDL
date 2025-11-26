# matrix.py
# Operaciones con matrices usando listas de listas.

def shape(A):
    rows = len(A)
    cols = len(A[0]) if rows > 0 else 0
    return rows, cols


def zeros(rows, cols, value=0.0):
    return [[value for _ in range(cols)] for _ in range(rows)]


def mat_add(A, B):
    rA, cA = shape(A)
    rB, cB = shape(B)
    if rA != rB or cA != cB:
        raise ValueError("dimensiones incompatibles para suma")
    C = zeros(rA, cA)
    for i in range(rA):
        for j in range(cA):
            C[i][j] = A[i][j] + B[i][j]
    return C


def mat_sub(A, B):
    rA, cA = shape(A)
    rB, cB = shape(B)
    if rA != rB or cA != cB:
        raise ValueError("dimensiones incompatibles para resta")
    C = zeros(rA, cA)
    for i in range(rA):
        for j in range(cA):
            C[i][j] = A[i][j] - B[i][j]
    return C


def mat_mul(A, B):
    """
    Multiplicación de matrices (A: r x n, B: n x c).
    """
    rA, cA = shape(A)
    rB, cB = shape(B)
    if cA != rB:
        raise ValueError("dimensiones incompatibles para multiplicación")
    C = zeros(rA, cB)
    for i in range(rA):
        for j in range(cB):
            s = 0.0
            for k in range(cA):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C


def mat_transpose(A):
    r, c = shape(A)
    T = zeros(c, r)
    for i in range(r):
        for j in range(c):
            T[j][i] = A[i][j]
    return T
    
# Matriz identidad n x n
def mat_identity(n):
    I = zeros(n, n)
    for i in range(n):
        I[i][i] = 1.0
    return I


# Inversa de A usando eliminacion Gauss Jordan. A debe ser cuadrada
def mat_inverse(A):
    n, m = shape(A)
    if n != m:
        raise ValueError("La inversa solo esta definida para matrices cuadradas")

    # Copia de A (para no modificar el original)
    # y construcción de la matriz aumentada [A | I]
    # Trabajamos con floats
    aug = []
    I = mat_identity(n)
    for i in range(n):
        fila = [float(x) for x in A[i]] + I[i]
        aug.append(fila)

    # Gauss Jordan
    for col in range(n):
        # 1) Buscar pivote (fila con mayor valor absoluto en esta columna)
        pivot_row = None
        pivot_val = 0.0
        for r in range(col, n):
            val = abs(aug[r][col])
            if val > pivot_val:
                pivot_val = val
                pivot_row = r

        if pivot_row is None or pivot_val == 0.0:
            raise ValueError("La matriz no es invertible (determinante = 0)")

        # 2) Intercambiar fila actual con fila pivote
        if pivot_row != col:
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        # 3) Normalizar fila pivote (hacer pivote = 1)
        pivot = aug[col][col]
        for j in range(2 * n):
            aug[col][j] /= pivot

        # 4) Hacer ceros en el resto de filas de esa columna
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor != 0.0:
                for j in range(2 * n):
                    aug[r][j] -= factor * aug[col][j]

    # Extraer la parte derecha, que ahora es A^{-1}
    inv = []
    for i in range(n):
        fila_inv = aug[i][n:]
        inv.append(fila_inv)

    return inv

