# MyRegression.py
# Regresión lineal simple (y = m*x + b)

# Calcula la recta y=m*x+b que mejor se ajusta a los puntos (xs,ys) en el sentido de minimos cuadrados
# Devuelve (m,b)
def regresion_lineal(xs, ys):
    if len(xs) != len(ys):
        raise ValueError("xs y ys deben tener la misma longitud")
    n = len(xs)
    if n == 0:
        raise ValueError("No se puede hacer regresion con 0 puntos")

    # Convertimos todo a float
    sx = 0.0
    sy = 0.0
    sxx = 0.0
    sxy = 0.0

    for x, y in zip(xs, ys):
        x = float(x)
        y = float(y)
        sx  += x
        sy  += y
        sxx += x * x
        sxy += x * y

    # Formulas de regresión lineal:
    # m = (n*Σxy - Σx*Σy) / (n*Σx^2 - (Σx)^2)
    # b = (Σy - m*Σx) / n
    denom = n * sxx - sx * sx
    if denom == 0:
        raise ValueError("No se puede hacer regresion (denominador 0)")

    m = (n * sxy - sx * sy) / denom
    b = (sy - m * sx) / n
    return [m, b]

# xs lista de valores  x
# params: lista [m, b] devuelta por regresion_lineal
def predecir_lineal(xs, params):
    m = float(params[0])
    b = float(params[1])

    ys_pred = []
    for x in xs:
        x = float(x)
        ys_pred.append(m * x + b)
    return ys_pred
