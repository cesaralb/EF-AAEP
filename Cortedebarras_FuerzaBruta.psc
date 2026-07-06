Algoritmo Cortedebarras_FuerzaBruta
	
	Definir n, i, j, longitud_restante Como Entero
	Definir ganancia_actual, ganancia_max Como Entero
	Definir precios Como Entero
	
	Escribir "=== CORTE DE BARRAS - FUERZA BRUTA ==="
	Escribir "Ingrese la longitud de la barra:"
	Leer n
	
	Dimension precios(n)
	
	Para i <- 1 Hasta n Hacer
		Escribir "Ingrese el precio para longitud ", i, ":"
		Leer precios(i)
	FinPara
	
	ganancia_max <- 0
	
	Para i <- 1 Hasta n Hacer
		ganancia_actual <- 0
		longitud_restante <- n
		j <- i
		Mientras longitud_restante > 0 Hacer
			Si j <= longitud_restante Entonces
				ganancia_actual <- ganancia_actual + precios(j)
				longitud_restante <- longitud_restante - j
			SiNo
				j <- j - 1
				Si j = 0 Entonces
					longitud_restante <- 0
				FinSi
			FinSi
		FinMientras
		Si ganancia_actual > ganancia_max Entonces
			ganancia_max <- ganancia_actual
		FinSi
	FinPara
	
	Escribir ""
	Escribir "Ganancia maxima: ", ganancia_max
	
FinAlgoritmo
