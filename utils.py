import numpy as np
import random

def crea_tablero(lado):
    tablero = np.full((lado,lado)," ")
    return tablero

def coloca_barco_plus(tablero, barco):
    # Nos devuelve el tablero si puede colocar el barco, si no devuelve False, y avise por pantalla
    tablero_temp = tablero.copy()
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]
    for pieza in barco:
        fila = pieza[0]
        columna = pieza[1]
        if fila < 0  or fila >= num_max_filas:
            print(f"No puedo poner la pieza {pieza} porque se sale del tablero")
            return False
        if columna <0 or columna>= num_max_columnas:
            print(f"No puedo poner la pieza {pieza} porque se sale del tablero")
            return False
        if tablero[pieza] == "O" or tablero[pieza] == "X":
            print(f"No puedo poner la pieza {pieza} porque hay otro barco")
            return False
        tablero_temp[pieza] = "O"
    return tablero_temp

def crea_barco_aleatorio(tablero):
    num_max_filas = tablero.shape[0]
    num_max_columnas = tablero.shape[1]
    while True:
        barco = []
        # Construimos el hipotetico barco
        pieza_original = (random.randint(0,num_max_filas - 1),random.randint(0, num_max_columnas - 1))
        print("Pieza original:", pieza_original)
        barco.append(pieza_original)

        orientacion = random.choice(["N","S","O","E"])
        print("Con orientacion", orientacion)

        fila = pieza_original[0]
        columna = pieza_original[1]
        eslora = random.randint(2, 4)
        
        for x in range(eslora -1):
            if orientacion == "N":
                fila -= 1
            elif orientacion  == "S":
                fila += 1
            elif orientacion == "E":
                columna += 1
            else:
                columna -= 1

            pieza = (fila,columna)
            barco.append(pieza)
            
        tablero_temp = coloca_barco_plus(tablero, barco)
        if type(tablero_temp) == np.ndarray:
            return tablero_temp
        print("Tengo que intentar colocar otro barco")

def flota(tablero): # Creamos flota de barcos en los tableros que le pasemos (tableros de barco)
    if tablero.shape[0] < 7: # Ajustamos numero de barcos a tamaño de tablero
        num_barcos = 3
    else:
        num_barcos = 4
    tablero_mod = crea_barco_aleatorio(tablero)
    for x in range(num_barcos):
        tablero_mod = crea_barco_aleatorio(tablero_mod)
    
    return tablero_mod # Retornamos el tablero modificado

def generar_coordenada(tab_shot): # Funcion para crear coordenadas aleatorias (aplicada al npc) 
    f_random = random.randint(0, tab_shot.shape[0] - 1)
    c_random = random.randint(0, tab_shot.shape[1] - 1)
    coordenada_random = (f_random, c_random)
    return coordenada_random

def disparar(tab_barco_rival, tab_shot, coordenada):
    c_mod = (coordenada[0] - 1, coordenada[1] -1) # modifico la coordenada del jugador (contando desde 1) a idioma de ordenador.
    if tab_barco_rival[c_mod] == "O":
        tab_barco_rival[c_mod] = "X"
        tab_shot[c_mod] = "X" # Para que aparezca la X en el tablero de disparo.
        print("Tocado. Elige una nueva coordenada")
        fila_nueva = int(input("Elige fila "))
        columna_nueva = int(input("Elige columna "))
        coordenada_nueva = check_coordenada(fila_nueva, columna_nueva, tab_shot) # Check de las nuevas coordenadas si hemos acertado
        print(f"La nueva coordenada es {coordenada_nueva}")
        disparar(tab_barco_rival, tab_shot, coordenada_nueva) # Llamamos de nuevo a la funcion para disparar

    elif tab_barco_rival[c_mod] == "X":
        print("Agonia, deja de perder el tiempo, dispara a otro sitio")
        
    else:
        tab_barco_rival[c_mod] = "~"
        tab_shot[c_mod] = "~" # Lo mismo si es agua
        print("Agua")
    
    return tab_shot

def check_coordenada(fila, columna, tab_shot):
    check = True
    while check:
        if fila not in range(1, tab_shot.shape[0] + 1):
            fila = int(input("Elige fila de nuevo "))
        elif columna not in range(1, tab_shot.shape[1] + 1):
            columna = int(input("Elige columna de nuevo "))
        else:
            coordenada = (fila, columna)
            check = False
    return coordenada

def recibir_disparo(tab_barco_jugador, tab_shot_npc, coordenada):
    if tab_barco_jugador[coordenada] == "O":
        tab_barco_jugador[coordenada] = "X"
        tab_shot_npc[coordenada] = "X"
        print("Tocado. Nueva coordenada")
        coordenada_nueva = generar_coordenada(tab_shot_npc)
        print(f"La nueva coordenada es {coordenada_nueva}")

        if tab_shot_npc[coordenada_nueva] == "X" or tab_shot_npc[coordenada_nueva] == "-":
            print(f"La nueva coordenada ya se ejecuto. Generando otra...")
            coordenada_nueva2 = generar_coordenada(tab_shot_npc)
            print(f"Se origino otra coordenada: {coordenada_nueva2}")
            recibir_disparo(tab_barco_jugador, tab_shot_npc, coordenada_nueva2)
        else:
            recibir_disparo(tab_barco_jugador, tab_shot_npc, coordenada_nueva)

    elif tab_barco_jugador[coordenada] == "X":
        print("Suerte, ha disparado donde ya lo hizo")
        
    else:
        tab_barco_jugador[coordenada] = "~"
        tab_shot_npc[coordenada] = "~"
        print("Agua")
    return tab_barco_jugador

def arregla_barcos(tablero):
    tablero[tablero == "X"] = "O"
    tablero[tablero == "O"] = " "
    tablero[tablero == "-"] = " " # Limpio coordenadas de "agua".
    return tablero
