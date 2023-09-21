import csv
import matplotlib.pyplot as plt
import numpy as np

# Leer el laberinto desde un archivo CSV
def leer_laberinto(nombre_archivo):
    laberinto = []
    with open(nombre_archivo, 'r') as archivo:
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            laberinto.append([int(c) for c in fila])
    return laberinto

# Encontrar una solución desde una entrada
def encontrar_solucion(laberinto, entrada, salida):
    n = len(laberinto)
    m = len(laberinto[0])

    def backtrack(x, y, camino_actual):
        if x < 0 or x >= n or y < 0 or y >= m or laberinto[x][y] == 1:
            return

        if (x, y) == salida:
            caminos.append(list(camino_actual))
            return

        laberinto[x][y] = 1  # Marcar la casilla actual como visitada

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = x + dx, y + dy
            camino_actual.append((ni, nj))
            backtrack(ni, nj, camino_actual)
            camino_actual.pop()

        laberinto[x][y] = 0  # Restaurar la casilla

    caminos = []

    backtrack(entrada[0], entrada[1], [(entrada[0], entrada[1])])

    return caminos

# Buscar todas las soluciones en el laberinto
def buscar_soluciones(laberinto):
    n = len(laberinto)
    m = len(laberinto[0])
    
    soluciones = []
    
    # Buscar entradas en el contorno de la matriz
    entradas = []
    for i in range(n):
        if laberinto[i][0] == 0:
            entradas.append((i, 0))
        if laberinto[i][m - 1] == 0:
            entradas.append((i, m - 1))
    for j in range(m):
        if laberinto[0][j] == 0:
            entradas.append((0, j))
        if laberinto[n - 1][j] == 0:
            entradas.append((n - 1, j))

    # Encontrar soluciones desde cada entrada
    for i, entrada in enumerate(entradas[:-1]):  # Evitar la última entrada
        for entrada2 in entradas[i + 1:]:  # Comenzar desde la siguiente entrada
            caminos = encontrar_solucion(laberinto, entrada, entrada2)
            if caminos:
                for camino in caminos:
                    soluciones.append((entrada, entrada2, camino))

    return soluciones

# Validar el laberinto
def validar_laberinto(laberinto):
    n = len(laberinto)
    m = len(laberinto[0])

    if n < 10 or m < 10:
        return False

    return True

# Presentar gráficamente el laberinto en modo interactivo
def mostrar_laberinto(laberinto):
    plt.ion()  # Activar el modo interactivo
    plt.imshow(laberinto, cmap='gray', interpolation='none')
    plt.pause(0.01)  # Agregar una pausa pequeña para permitir la actualización de la ventana

# Función para mostrar un camino específico en una imagen
def mostrar_camino(laberinto, camino):
    plt.figure()  # Crear una nueva figura para el camino
    plt.imshow(laberinto, cmap='gray', interpolation='none')
    
    camino_array = np.array(camino)
    plt.plot(camino_array[:, 1], camino_array[:, 0], color='red', linewidth=2)  # Resaltar el camino en rojo

    plt.show()

if __name__ == "__main__":
    nombre_archivo = "laberinto.csv"
    laberinto = leer_laberinto(nombre_archivo)
    if validar_laberinto(laberinto):
        mostrar_laberinto(laberinto)
        soluciones = buscar_soluciones(laberinto)
        if len(soluciones) > 0:
            print(f"El laberinto tiene {len(soluciones)} soluciones.")
            for i, (entrada, salida, camino) in enumerate(soluciones):
                print(f"Solución {i + 1}: Desde {entrada} hasta {salida}")
                print("Camino recorrido:")
                print(", ".join([str(paso) for paso in camino]))
                print()
                if i == 0:  # Mostrar solo el primer camino
                    mostrar_camino(laberinto, camino)
        else:
            print("No hay soluciones.")
    else:
        print("El laberinto no es válido.")

    plt.ioff()
    plt.show()
