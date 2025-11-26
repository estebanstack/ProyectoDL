PI = 3.141592653589793
E  = 2.718281828459045


def factorial(n):
    n = int(n)
    if n < 0:
        raise ValueError("factorial indefinido para n < 0")
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


# Potencia x^y.
# Para enteros usa multiplicación repetida, para otros casos usa el operador ** de Python
def potencia(x, y):
    
    # si y es entero
    if int(y) == y:
        y = int(y)
        if y == 0:
            return 1
        if y < 0:
            return 1 / potencia(x, -y)
        res = 1
        for _ in range(y):
            res *= x
        return res
    else:
        return x ** y

# Reduce x al rango [-PI, PI] para mejor precision
def reducir_angulo(x):
    while x > PI:
        x -= 2 * PI
    while x < -PI:
        x += 2 * PI
    return x

# Aproximacion de sin(x) usando serie de Taylor x en radianes
def sin(x):
    x = float(x)
    x = reducir_angulo(x)

    terms = 10  # mas terminos = mas precision
    res = 0.0
    for k in range(terms):
        num = potencia(-1, k) * potencia(x, 2 * k + 1)
        den = factorial(2 * k + 1)
        res += num / den
    return res

# Aproximacion de cos(x) usando serie de Taylor
def cos(x):
    x = float(x)
    x = reducir_angulo(x)

    terms = 10
    res = 0.0
    for k in range(terms):
        num = potencia(-1, k) * potencia(x, 2 * k)
        den = factorial(2 * k)
        res += num / den
    return res


def tan(x):
    c = cos(x)
    if c == 0:
        raise ZeroDivisionError("tan indefinido para cos(x) = 0")
    return sin(x) / c

# Raíz cuadrada por metodo de Newton-Raphson
def sqrt(x):
    x = float(x)
    if x < 0:
        raise ValueError("sqrt indefinido para x < 0")
    if x == 0:
        return 0.0
    guess = x / 2.0
    for _ in range(20):
        guess = 0.5 * (guess + x / guess)
    return guess
