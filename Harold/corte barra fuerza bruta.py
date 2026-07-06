def corte_fuerza_bruta(longitud, precios):
    if longitud == 0:
        return 0, []

    mejor_ganancia = 0
    mejores_cortes = []

    for primer_corte in range(1, longitud + 1):
        ganancia_restante, cortes_restantes = corte_fuerza_bruta(
            longitud - primer_corte,
            precios
        )

        ganancia_total = precios[primer_corte] + ganancia_restante

        if ganancia_total > mejor_ganancia:
            mejor_ganancia = ganancia_total
            mejores_cortes = [primer_corte] + cortes_restantes

    return mejor_ganancia, mejores_cortes


def mostrar_tabla_precios(precios):
    print("\nTabla de precios")
    print("----------------")
    for longitud in range(1, len(precios)):
        print("Longitud", longitud, "-> S/.", precios[longitud])


print("CORTE DE BARRAS - FUERZA BRUTA")
print("--------------------------------")

n = int(input("Ingrese la longitud de la barra: "))

precios = [0]

for i in range(1, n + 1):
    precio = int(input("Ingrese el precio para longitud " + str(i) + ": "))
    precios.append(precio)

mostrar_tabla_precios(precios)

ganancia_maxima, cortes = corte_fuerza_bruta(n, precios)

print("\nResultado")
print("---------")
print("Longitud de la barra:", n)
print("Cortes recomendados:", cortes)
print("Ganancia maxima: S/.", ganancia_maxima)

print("\nExplicacion:")
print("El algoritmo prueba todos los posibles primeros cortes.")
print("Luego resuelve de forma recursiva la parte restante de la barra.")
print("Finalmente se queda con la combinacion que genera mayor ganancia.")
