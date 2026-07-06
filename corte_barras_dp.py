"""
==========================================================================
 CORTE DE BARRAS PARA PRODUCCION (Rod Cutting Problem)
 Estrategia de programacion: PROGRAMACION DINAMICA
==========================================================================

PROBLEMA:
    Se tiene una barra de acero de longitud N y una tabla de precios
    precio[i] = valor de venta de una pieza de longitud i (1 <= i <= N).
    Se debe decidir en que puntos cortar la barra (o si conviene NO
    cortarla) para MAXIMIZAR el ingreso total por la venta de las piezas
    resultantes.

POR QUE PROGRAMACION DINAMICA:
    - Subestructura optima: la mejor forma de cortar una barra de
      longitud n es cortar un primer trozo de tamano i (1<=i<=n) y
      resolver de manera optima el resto (n - i). El optimo global se
      construye a partir de optimos de subproblemas mas pequenos.
    - Subproblemas superpuestos: al probar distintos primeros cortes,
      el mismo subproblema "cortar de forma optima una barra de
      longitud k" se repite muchas veces, por lo que conviene
      memorizarlo en una tabla en lugar de recalcularlo (como en la
      recursion de fuerza bruta, que es O(2^n)).

RELACION DE RECURRENCIA:
    ingreso_optimo(0) = 0
    ingreso_optimo(n) = max( precio[i] + ingreso_optimo(n - i) )   para i = 1..n

COMPLEJIDAD:
    - Fuerza bruta (probar todos los cortes posibles, recursivo):  O(2^n)
    - Programacion Dinamica (bottom-up con tabla):                 O(n^2) en tiempo, O(n) en espacio

Autor: Diego (asistido por Claude) - Informe de Medicion ALEST
==========================================================================
"""

import random
import time
# --------------------------------------------------------------------
# 1. ALGORITMO EXACTO CON PROGRAMACION DINAMICA (BOTTOM-UP)
# --------------------------------------------------------------------
def corte_barras_dp(precios, n):
    """
    precios: lista donde precios[i-1] es el precio de una pieza de
             longitud i (precios[0] = precio de longitud 1, etc.)
    n:       longitud total de la barra a cortar

    Retorna: (ingreso_maximo, lista_de_cortes)
             lista_de_cortes = longitudes de cada pieza en la solucion optima
    """
    # dp[j] = ingreso maximo obtenible con una barra de longitud j
    dp = [0] * (n + 1)
    # primer_corte[j] = tamano del primer trozo usado en la solucion optima de dp[j]
    primer_corte = [0] * (n + 1)

    for j in range(1, n + 1):
        mejor = float("-inf")
        mejor_i = 0
        for i in range(1, j + 1):
            precio_i = precios[i - 1] if i - 1 < len(precios) else float("-inf")
            candidato = precio_i + dp[j - i]
            if candidato > mejor:
                mejor = candidato
                mejor_i = i
        dp[j] = mejor
        primer_corte[j] = mejor_i

    # Reconstruccion de los cortes optimos a partir de la tabla "primer_corte"
    cortes = []
    restante = n
    while restante > 0:
        cortes.append(primer_corte[restante])
        restante -= primer_corte[restante]

    return dp[n], cortes


# --------------------------------------------------------------------
# 2. VERSION RECURSIVA CON MEMORIZACION (top-down) - misma complejidad
#    O(n^2), incluida solo para fines comparativos/didacticos.
# --------------------------------------------------------------------
def corte_barras_memo(precios, n, memo=None):
    if memo is None:
        memo = {}
    if n == 0:
        return 0
    if n in memo:
        return memo[n]

    mejor = float("-inf")
    for i in range(1, n + 1):
        precio_i = precios[i - 1] if i - 1 < len(precios) else float("-inf")
        mejor = max(mejor, precio_i + corte_barras_memo(precios, n - i, memo))

    memo[n] = mejor
    return mejor


# --------------------------------------------------------------------
# 3. VERSION DE FUERZA BRUTA (recursion pura, SIN memorizar)
#    Solo para comparar tiempos en el analisis empirico. O(2^n).
# --------------------------------------------------------------------
def corte_barras_fuerza_bruta(precios, n):
    if n == 0:
        return 0
    mejor = float("-inf")
    for i in range(1, n + 1):
        precio_i = precios[i - 1] if i - 1 < len(precios) else float("-inf")
        mejor = max(mejor, precio_i + corte_barras_fuerza_bruta(precios, n - i))
    return mejor


# --------------------------------------------------------------------
# 4. DEMOSTRACION DEL SISTEMA
# --------------------------------------------------------------------
def demo_sistema():
    print("=" * 70)
    print(" DEMO: CORTE DE BARRAS PARA PRODUCCION (Programacion Dinamica)")
    print("=" * 70)

    # Tabla de precios clasica del ejemplo de CLRS: precios[i-1] = precio de longitud i
    precios = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    n = 10

    print(f"\nLongitud de la barra: {n}")
    print("Tabla de precios (longitud: precio):")
    for i, p in enumerate(precios, start=1):
        print(f"   {i}: {p}")

    t0 = time.perf_counter()
    ingreso_max, cortes = corte_barras_dp(precios, n)
    t1 = time.perf_counter()

    print(f"\nIngreso maximo posible: {ingreso_max}")
    print(f"Cortes optimos (longitudes de cada pieza): {cortes}")
    print(f"Suma de piezas: {sum(cortes)} (debe ser igual a n = {n})")
    print(f"Tiempo de calculo (DP): {(t1 - t0) * 1000:.4f} ms")

    # Comparacion contra vender la barra completa sin cortar
    ingreso_sin_cortar = precios[n - 1] if n - 1 < len(precios) else 0
    print(f"\nIngreso si se vendiera la barra completa sin cortar: {ingreso_sin_cortar}")
    if ingreso_max > ingreso_sin_cortar:
        print(f"-> Cortar la barra genera {ingreso_max - ingreso_sin_cortar} unidades MAS de ganancia.")
    else:
        print("-> No conviene cortar la barra, es mejor venderla completa.")


# --------------------------------------------------------------------
# 5. ANALISIS EMPIRICO: DP (O(n^2)) vs FUERZA BRUTA (O(2^n))
#    (para la seccion 4.1 del informe)
# --------------------------------------------------------------------
def analisis_empirico(n_max_bruta=22, n_max_dp=1000):
    print("\n" + "=" * 70)
    print(" ANALISIS EMPIRICO: PROGRAMACION DINAMICA vs FUERZA BRUTA")
    print("=" * 70)

    random.seed(1)
    precios_grandes = [random.randint(1, 50) for _ in range(max(n_max_bruta, n_max_dp))]

    print(f"\n{'n':>5} | {'tiempo Fuerza Bruta (s)':>25} | {'tiempo DP (s)':>15}")
    print("-" * 55)
    for n in range(5, n_max_bruta + 1, 2):
        t0 = time.perf_counter()
        corte_barras_fuerza_bruta(precios_grandes, n)
        t1 = time.perf_counter()

        t2 = time.perf_counter()
        corte_barras_dp(precios_grandes, n)
        t3 = time.perf_counter()

        print(f"{n:>5} | {t1 - t0:>25.5f} | {t3 - t2:>15.7f}")

    print(f"\n(A partir de aqui la fuerza bruta ya no es practica; "
          f"solo se mide la version con Programacion Dinamica)")
    print(f"\n{'n':>5} | {'tiempo DP (s)':>15}")
    print("-" * 25)
    for n in [50, 100, 300, 500, 1000]:
        if n <= len(precios_grandes):
            t0 = time.perf_counter()
            corte_barras_dp(precios_grandes, n)
            t1 = time.perf_counter()
            print(f"{n:>5} | {t1 - t0:>15.5f}")


if __name__ == "__main__":
    demo_sistema()
    analisis_empirico()
