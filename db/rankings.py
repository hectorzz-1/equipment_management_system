from .Table_players import PlayerSelect
from .initialize_db import DataBaseMCB
from .table_statistics import StatisticSelect


# Sirve para clasificar los jugadores por un dato en especifico
# a la clase se le tiene que pasar un base de datos y el attributo para clasificar
# retorna una [{:}]
class Ranking:

    # Datos por los cuales se pueden clasificar los jugadores
    ALLOWED_COLUMNS = {"goals", "assists", "matches", "minutes", "yellow_card", "red_card"}

    def __init__(self,db, attribute):
        # Base de datos
        self.db = db
        # Validar si attribute es un dato clasificlable
        if attribute not in self.ALLOWED_COLUMNS:
            raise ValueError("column not valid for rank")
        self.attribute = attribute
        # Donde se guardarán los datos clasificados de los jugadores
        self.players_list = []

    # Clasififca los datos
    def rank(self):
        # Obtenemos los jugadores de la base de datos
        data_base_players = PlayerSelect(db=self.db).get_all()

        for i in data_base_players:
            # Obtenemos las estadisticas de cada jugador
            player_statistics = StatisticSelect(db=self.db).get_by_id(id=i[0],colmn=self.attribute)
            # Ordenamos los datos en un diccionario
            player = {
                "id" : i[0],
                "name" : i[1],
                "last_name" : i[2],
                "attribute" : player_statistics[0][0]
                }
            # Guardamos los datos ordenados en la lista
            self.players_list.append(player)

        # Retornamos una [{:}] con los datos ya clasificados por attribute
        return sorted(self.players_list, key=lambda x: x["attribute"], reverse=True)
    

"""
from db.initialize_db import DataBaseMCB
from db.rankings import Ranking

with DataBaseMCB() as db:
    print(Ranking(db=db, attribute="goals").rank())
"""