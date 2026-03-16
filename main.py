import numpy as np
import random
import Funciones
import time
import math

exit = False
while exit == False: # Condicion de juego
    print("HUNDIR LA FLOTA")
    input("Presiona cualquier boton para continuar")
    menu = ["JUGAR",
            "CARGAR",
            "OPCIONES",
            "SALIR"]
    print(menu)
    seleccion = input("Selecciona opcion: JUGAR CARGAR OPCIONES SALIR ").lower()
    while seleccion != "jugar":
        if seleccion == "cargar":
            print("No hay partidas guardadas")
        elif seleccion == "opciones":
            print("Error, no tiene permisos para configurar")
        elif seleccion == "salir":
            print("¡Hasta pronto!")
            break
        else:
            print("Opcion no valida")
        seleccion = input("Selecciona opcion: JUGAR CARGAR OPCIONES SALIR ").lower()

    else:
        nombre_player = input("Introduce tu nombre de jugador ")
        print(f"Bienvenido a HUNDIR LA FLOTA, {nombre_player}. Espero que disfrutes del juego. \n Las reglas son sencillas: intenta acabar con los barcos del rival antes de que acabe con los tuyos. \n ¿Estás listo? Iniciando partida...")
        time.sleep(1)

        casillas = int(input("¿De que tamaño quieres el tablero? Elige: 25, 36, 49, 64, 81, 100 "))
        if casillas >= 25:
            dimension = int(math.sqrt(casillas))
        else:
            dimension = 5

        p1_boat = Funciones.crea_tablero(dimension) # Creamos tablero de jugador para barcos
        print("\n Tu tablero de barcos \n", p1_boat)
        time.sleep(1)
        p1_shot = Funciones.crea_tablero(dimension) # Creamos tablero de jugador para disparos
        print("\n Tu tablero de disparo \n", p1_shot)
        time.sleep(1)
        npc_boat = Funciones.crea_tablero(dimension) # Creamos tableros del NPC
        npc_shot = Funciones.crea_tablero(dimension)

        p1_boat_mod = Funciones.flota(p1_boat) # Asignamos tablero modificado al tablero con barcos del jugador
        print("\n Aquí tienes tu tablero de juego con los barcos de forma aleatoria\n", p1_boat_mod)
        time.sleep(1)
        npc_boat_mod = Funciones.flota(npc_boat) # Lo mismo con el tablero del NPC

        start = random.randint(1,2) # Tirada de moneda para decidir quien empieza
        p1 = False
        turno = 1

        if start == 1:
            p1 = True
            print(f"Empieza jugando {nombre_player}")
            time.sleep(1)
        else:
            print("Empieza jugando tu rival")
            time.sleep(1)

        while "O" in p1_boat_mod and "O" in npc_boat_mod: # Si existen barcos "O" en ambos tableros, seguimos jugando

            print(f"Turno {turno}")
            time.sleep(1)

            if p1:
                print("Elige unas coordenadas de ataque")
                print(p1_shot) # Se imprime el tablero de disparo para mayor precision
                fila = int(input("Elige fila "))
                columna = int(input("Elige columna "))

                coordenada = Funciones.check_coordenada(fila, columna, p1_shot)
                print(f"Tu coordenada es {coordenada}") 
                time.sleep(1)

                Funciones.disparar(npc_boat_mod, p1_shot, coordenada)
                p1 = False # Convertimos la variable jugador en False para que pase al siguiente jugador
            
            else:
                coordenada_random = Funciones.generar_coordenada(npc_shot)
                print(f"La coordenada del rival es {coordenada_random}")
                time.sleep(1)
                Funciones.recibir_disparo(p1_boat_mod, npc_shot, coordenada_random)
                print("Tablero de barcos")
                print(p1_boat_mod)
                p1 = True # Volvemos a convertir en True para que el siguiente turno sea del jugador
            turno += 1
        
        else:
            if "O" not in p1_boat_mod:
                print(f"¡Has perdido! El numero de turnos ha sido {turno}")
            else:
                print(f"Enhorabuena, has acabado con tu rival. El numero de turnos ha sido {turno}")
    
    if seleccion == "salir":
        exit = True
    else:
        reset = input("¿Quieres volver a jugar? y/n ").lower()
        if reset == "y":
            Funciones.arregla_barcos(p1_boat_mod)
            Funciones.arregla_barcos(p1_shot)
            Funciones.arregla_barcos(npc_boat_mod)
            Funciones.arregla_barcos(npc_shot) # Reseteamos todos los tableros para volver a jugar
        else:
            print("¡Hasta pronto!")
            exit = True


    


