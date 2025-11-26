<img width="769" height="483" alt="image" src="https://github.com/user-attachments/assets/d886f152-2305-49ad-8294-206b4b4c26bd" />
# ESTEBAN CASTRO JUAN GONZALEZ

# DLang – Lenguaje de dominio especifico para realizar procesos de Deep Learning

## 1. Descripción general

Este proyecto implementa un **lenguaje de dominio específico (DSL)** llamado **DLang**, diseñado para permitir al usuario realizar tareas típicas de cálculo numérico, álgebra de matrices, aprendizaje automático y visualización, *todo sin usar librerías externas* como `math`, `numpy` o `matplotlib`.

DLang funciona gracias a:

* Una **gramática ANTLR4**.
* Un **intérprete propio** en Python (Visitor).
* Bibliotecas internas implementadas totalmente a mano.

El resultado es un lenguaje completo con:

* Aritmética, trigonometría, raíces.
* Matrices: suma, resta, multiplicación, transpuesta, inversa.
* Archivos simulados.
* Gráficas ASCII estilo matplotlib.
* Regresión lineal.
* Perceptrón multicapa (MLP) desde cero.
* Red competitiva para clustering.

---

## 2. Compilación de la gramática

El archivo central del lenguaje es:

```
DLang.g4
```

Para generar el parser y visitor:

```bash
antlr4 -Dlanguage=Python3 -visitor DLang.g4
```

---

## 3. Ejecución del intérprete

### Ejecutar un programa `.dl`:

```bash
python Main.py archivo.dl
```

### Modo interactivo (REPL):

```bash
python Main.py
```

---

## 4. Estructura del proyecto

### 4.1 Núcleo del lenguaje

| Archivo            | Descripción                                             |
| ------------------ | ------------------------------------------------------- |
| **DLang.g4**       | Gramática completa del lenguaje DLang escrita en ANTLR4 |
| **Main.py**        | Punto de entrada, ejecuta archivos o abre REPL          |
| **EvalVisitor.py** | Intérprete: ejecuta sentencias y expresiones del DSL    |

EvalVisitor:

* Maneja variables, funciones, control de flujo.
* Llama funciones internas según nombre (`sin`, `plot`, `mat_mul`, etc.)
* Diferencia entre valores escalares, listas y matrices.

---

## 4.2 Bibliotecas internas implementadas a mano

### MyMath.py

* Implementación manual de:

  * `sin(x)`, `cos(x)` → series de Taylor.
  * `tan(x)`
  * `sqrt(x)` → Newton-Raphson.
  * `exp`, `factorial`, `potencia`.

Sin usar `math`.

---

### Matrix.py

Soporte completo para matrices:

* `mat_add(A, B)`
* `mat_sub(A, B)`
* `mat_mul(A, B)` (triple for)
* `mat_transpose(A)`
* `mat_inverse(A)` usando Gauss-Jordan

En el lenguaje, las listas dobles `[ [..], [..] ]` se interpretan como matrices automáticamente.

---

### MyFile.py — Filesystem simulado

Usa un diccionario interno:

```python
FS["ruta.txt"] = "contenido"
```

Funciones:

* `write_text`
* `append_text`
* `read_text`
* `read_lines`

---

### MyPlot.py – Motor de gráficos ASCII estilo matplotlib

Este módulo replica una API similar a `matplotlib.pyplot`, pero todo se imprime en ASCII:

Funciones disponibles:

* `figure(width, height)`
* `plot(xs, ys)`
* `scatter(xs, ys)`
* `title(text)`
* `xlabel(text)`
* `ylabel(text)`
* `show()`
* `clf()`
* `close()`

Características:

* Renderizado en una rejilla de caracteres.
* Ejes X/Y automáticos.
* Múltiples series con distintos marcadores.
* Algoritmo de Bresenham para unir puntos.

---

### MyRegression.py

Implementa regresión lineal:

* `regresion_lineal(xs, ys)` → retorna `m, b`
* `predecir_lineal(xs, (m,b))` → calcula ys pronosticados

Sin librerías, usando las fórmulas de mínimos cuadrados.

---

### MyMLP.py — Perceptrón Multicapa

Red neuronal que tiene:

* Función de activación: sigmoide implementada con Taylor.
* Backpropagation manual.
* Inicialización determinista.
* Métodos:

  * `train(X, Y, lr, epochs)`
  * `predict(X)`
  * `predict_real_mlp()`

Se usa para aprender el problema XOR.

---

### MyClusterNN.py – Red competitiva

Una red tipo "k-means neural":

* Centros iniciales deterministas.
* Entrenamiento por regla del ganador (winner-takes-all).
* `train_cluster_net(model, X, lr, epochs)`
* `predict_cluster(model, X)`

---

## 5. Sintaxis del DSL

### Variables:

```dl
x = 5
msg = "hola"
lista = [1, 2, 3]
```

### Condicionales:

```dl
if x > 3 {
    print("mayor")
}
```

### Funciones definidas por el usuario:

```dl
def doble(n) {
    return n * 2
}
print(doble(5))
```

### While:

```dl
i = 0
while i < 5 {
    print(i)
    i = i + 1
}
```

---

## 6. Ejemplos completos

### Regresión + gráfica ASCII

```dl
xs = [1,2,3,4,5]
ys = [2,3,5,4,5]

params = regresion_lineal(xs, ys)
ys_pred = predecir_lineal(xs, params)

plot(xs, ys, label="Datos")
plot(xs, ys_pred, label="Predicción")
title("Regresión Lineal")
xlabel("x")
ylabel("y")
show()
```

### MLP XOR

```dl
X = [[0,0],[0,1],[1,0],[1,1]]
Y = [0,1,1,0]

m = create_mlp(2,4,1)
train_mlp(m, X, Y, 0.5, 8000)
print(predict_mlp(m, X))
```

---

## 7. Decisiones de diseño

* No usar ninguna librería externa.
* Implementar todo desde cero:

  * Trigonometría
  * Algebra lineal
  * Plotting
  * Redes neuronales


---
