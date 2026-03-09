import os
import json
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv

from db.table_statistics import (Statistics, StatisticsInsert,
                                  StatisticsUpdateA, StatisticSelect)
from db.Table_players import Player, PlayerInsert, PlayerSelect
from db.initialize_db import DataBaseMCB
from db.rankings import Ranking

from agent.initialize_IA import ConnectBrain
from agent.actions_IA import GetQuery
from agent.valid_data_IA import MatchReport

if __name__ == "__main__":

    # Bucle para elegir una acción
    for i in range(3):
        # Mostrar las opciones por pantalla
        print("Actions: register(1), rank(2), up date(3), check statistics(4)")
        # Definir las opciones correctas
        ACTION_ALLOWED = ("1","2","3","4")
        # Que el usuario retorne una opción
        action = input(": ")

        # Si lo que puso el usuario no es correcto
        # se le informa y se repite el bucle
        if str(action) not in ACTION_ALLOWED:
            print("Choose from the option 1, 2 ,3 or 4\n")
            continue
        
        # Si todo es correcto se rompe el bucle
        break

    # Si el usuario quiere registrar jugadores
    if str(action) == "1":

        # Le pedimos al usuario los datos del jugador
        name_r = input("Player name: ")
        last_name_r = input("Player last name: ")
        number_r = input("Number player: ")

        # Ordenamos los datos que nos dio el usuario
        data_player_register = {
            "name" : str(name_r),
            "last_name" : str(last_name_r),
            "number" : int(number_r)
        }

        # Entramos a la base de datos
        with DataBaseMCB() as db:

            # Creamos al jugador
            player_register = Player(name=data_player_register['name'], last_name=data_player_register["last_name"], id=uuid4(), number=data_player_register["number"])
            # inicializamos las estadisticas del jugador todas a 0
            init_statistics_player = Statistics(id_player=player_register.id)

            # Insertamos al jugador en la base de datos
            PlayerInsert(db=db, data=player_register).action()
            # Insertamos las estadisticas del jugador a la base de datos
            StatisticsInsert(db=db, data=init_statistics_player).action()

        print("The player was added correctly")
    
    # Si el usuario quiere ver un ranking de algun atributo
    elif str(action) == "2":

        # Si el usuario se equivoca en algun atributo
        # se repite el bucle hasta 3 veces
        for i in range(3):
            # Le mostramos las opciones quel usuario puede rankear
            print("What data do you want to rank?")
            print(f"options: {Ranking.ALLOWED_COLUMNS}")
            # Requerimos que escriba alguna de las opciones
            data_to_rank = input(": ")

            # Entramos a la base de datos
            with DataBaseMCB() as db:
                # Intentamos hacer el ranking con el atributo que nos paso el usuario
                try:
                    ranking_player = Ranking(db=db, attribute=str(data_to_rank)).rank()
                # Si algo falla entonces lo imprimimos
                # en pantalla y se repite el bucle
                except ValueError as e: 
                    print(f"ERROR: {e}\n")
                    continue
            # Si todo sale bien
            # rompemos el bucle
            break
        
        # Inicializamos la poscision en el ranking
        position_ranking = 1
        # Inicializamos la lista donde estara la 
        # informacion de cada jugador del ranking
        ranking_list = []
        # Añadimos los jugadores a la lista
        for player in ranking_player:
            # Si el jugador no tiene del atributo con el que tabajamos
            # entonces no se añade a la lista
            if player["attribute"] <= 0:
                pass
            # Si el jugador si tiene del atributo con el que trabajamos
            # entonces los añadimos a la lista
            else: 
                # Ej: 1. santiago sanabria mendez (e2319e66-cd63-4863-9d69-0016e7390c50) red_card: 2
                ranking_list.append(f"{position_ranking}. {player['name']} {player['last_name']} ({player['id']}) {data_to_rank}: {player['attribute']}")
                # aumentamos la poscision en el ranking
                # del siguiente jugador
                position_ranking += 1
        
        # Si la lista esta vacia entonces imprimimos por 
        # pantalla que no hay guadores con ese atributo
        if not ranking_list:
            print(f"There are no player with {data_to_rank}")
        # Si si hay jugadores, entonces los imprimimos por pantalla
        else:
            for player_ranking_position in ranking_list:
                print(player_ranking_position)

    elif str(action) == "3":
        # Cargamos el .env con la ruta absoluta
        BASE_DIR = Path(__file__).resolve().parent
        load_dotenv(BASE_DIR / ".env")

        # Obtenemos la API KEY
        api_key = os.getenv("API_KEY_OPENAI")
        # Nos conectamos al cerebro de OpenAIS
        brain = ConnectBrain(key=api_key).connect()
        # Cargamos el json con las configuraciones del agente
        BASE_JSON = Path(__file__).resolve().parent / "config_IA.json"

        # Pedimos al usuario el reporte
        print("Please forward the report")
        user_report = input(": ")

        with open(BASE_JSON, "r") as file: 
            # Guardamos las configuración en una variable
            ia_config = json.load(file)
            # Le añadimos en la memoria de conversación nuestro reporte
            ia_config["memory"].append({"role" : "user", "content" : user_report})

        # Le hacemos la consulta al cerbro de OpenAI
        agent_report = GetQuery(brain=brain, agent=ia_config, format=MatchReport).make_query()

        try:
            # Iniciamos session en la base de datos
            with DataBaseMCB() as db:
                # Actualizamos la base de datos
                StatisticsUpdateA(db=db, report=agent_report).action()
            # Confirmamos actalización
            print("database successfully updated")

        # Si algo falla retornamos el error
        except ValueError as e: 
            print("The database could not be updated")
            print(f"ERROR: {e}\n")
    
    # Si el usuario quiere consultar las estadisticas de sus jugadores
    elif str(action) == "4":
        # Inicializamos la lista con los datos y estadisticas de los jugadores
        list_check_players = []

        # Entramos a la base de datos
        with DataBaseMCB() as db:
            # Obtenemos los datos de los jugadores
            players_information = PlayerSelect(db=db).get_all()
            # Obtenemos las estadisticas de los jugadores
            players_statistics = StatisticSelect(db=db).get_all()

        for player in players_information:
            # Obtenemos el id del jugador
            player_id = player["id"] 
            
            for i in players_statistics:
                # Comparamos el id del jugador con el de las caracteristicas 
                if player_id == i["id_player"]:
                    # Si coinside guardamos las estadisticas en una variable
                    # y rompemos el bucle
                    player_statistics = i
                    break
            
            # Añadimos la información a la lista
            list_check_players.append(f"({player['id']}). {player['name']} {player['last_name']} - numero:{player['number']}\nStatistics: goals: {player_statistics['goals']}, assists: {player_statistics['assists']}, matches: {player_statistics['matches']}, minutes: {player_statistics['minutes']}, yellow_card: {player_statistics['yellow_card']}, red_card: {player_statistics['red_card']}")
        
        # Si la lista esta vacia entonces imprimimos por 
        # pantalla que no hay guadores en la base de datos
        if not list_check_players:
            print(f"There are no player in database")
        # Si si hay jugadores, entonces los imprimimos por pantalla
        else:
            for player in list_check_players:
                print(player)
