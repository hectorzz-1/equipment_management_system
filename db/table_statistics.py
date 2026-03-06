from dataclasses import dataclass, asdict 
from uuid import UUID


# Esta clase retorna un objeto
# con las diferentes estadisticas del jugador inicializadas en 0
# statistics_init = Statistics()
@dataclass
class Statistics:
    id_player : UUID
    # goles del jugador
    goals : int = 0
    # asistencias del jugador
    assists : int = 0
    # juegos disputados del jugador
    matches : int = 0
    # minutos disputados del jugador 
    minutes : int = 0
    # tarjetas amarillas mostradas al jugador
    yellow_card : int = 0 
    # tarjetas rojas mostradas al jugador
    red_card :int = 0

    # Valida los datos
    def __post_init__(self):
        
        # Valida que goals sea int
        if isinstance(self.goals, str):
            raise ValueError("goals must be integer")
        # Valida que goals no sea menor que 0
        if self.goals < 0 :
            raise ValueError("goals cannot be less than 0")
        
        # Valida que assists sea int
        if isinstance(self.assists, str):
            raise ValueError("assists must be integer")
        # Valida que assists no sea menor que 0
        if self.assists < 0 :
            raise ValueError("assists cannot be less than 0")
        
        # Valida que matches sea int
        if isinstance(self.matches, str):
            raise ValueError("matches must be integer")
        # Valida que matches no sea menor que 0
        if self.matches < 0 :
            raise ValueError("matches cannot be less than 0")
        
        # Valida que minutes sea int
        if isinstance(self.minutes, str):
            raise ValueError("minutes must be integer")
        # Valida que minutes no sea menor que 0
        if self.minutes < 0 :
            raise ValueError("minutes cannot be less than 0")
        
        # Valida que yellow_card sea int
        if isinstance(self.yellow_card, str):
            raise ValueError("yellow_card must be integer")
        # Valida que yellow_card no sea menor que 0
        if self.yellow_card < 0 :
            raise ValueError("yellow_card cannot be less than 0")
        
        # Valida que red_card sea int
        if isinstance(self.red_card, str):
            raise ValueError("red_card must be integer")
        # Valida que red_card no sea menor que 0
        if self.red_card < 0 :
            raise ValueError("red_card cannot be less than 0")
        # Valida que el jugador no tenga más rojas 
        # que partidos ya que sería imposible
        if self.red_card > self.matches:
            raise ValueError("Red_cards cannot exceed matches played")


# Esta clase contendrá el lenguaje sql
# que se usará para la tabla statistics
class StatisticSQL:

    # SQL que sirve para hacer un insert en la tabla statistics
    insert = """
        INSERT INTO statistics (id_player ,goals, assists, matches, minutes, yellow_card, red_card)
        VALUES (%(id_player)s ,%(goals)s, %(assists)s, %(matches)s, %(minutes)s, %(yellow_card)s, %(red_card)s)
        """
    

# Gestiona la tabla statistics
# inserta
# elimina
# retorna
class StatisticsAction:
    
    def __init__(self, db, data, sql: StatisticSQL):
        # Pasar la base de datos
        self.db = db
        # Pasar los datos que se insertarán
        self.data = data
        # Pasar la clase StatisticSQL para disponer del lenguaje SQL
        self.sql = sql

    # Inserta las estadisticas de un jugador en la base de datos
    def insert(self):

        # Pasamos el id_player de tipo UUID a tipo str
        # para que la base de datos lo pueda manejar
        if isinstance(self.data.id_player, UUID):
            self.data.id_player = str(self.data.id_player)
        
        # Intenta hacer un insert
        # en la tabla statistics
        try: 
            self.db.cur.execute(
                self.sql.insert, # sql
                # volvemos el objeto un diccionario
                asdict(self.data)
            )
        
        # Si no logra hacer el insert 
        # entonces retorna el error
        except Exception as e:
            self.db.conn.rollback()
            print("Error:", e)

"""
from uuid import UUID

from agent.valid_data_IA import MatchReport
from db.table_statistics import Statistics, StatisticsAction

# nos conectamos a la base de datos
with DataBaseMCB() as db:
    # inicializamos las estadsticas de un jugador
    hector_statistics = Statistics(id_player=UUID("e2319e66-cd63-4863-9d69-0016e7390c50"))

    # Insertamos las estadisticas a la base de datos
    StatisticsAction(db=db, data=hector_statistics, sql=StatisticSQL).insert()"""            


# Su funcion es que con un modelo de pydantic con datos ordenados
# los agarre y actualice la base de datos automaticamente
class StatisticsUpdateA:
    
                          # : MatchReport
    def __init__(self,report , db):
        # Modelo Pydantic
        self.report = report
        # Conexión con una base de datos
        self.db = db

    # Actualiza la base de datos
    def action(self):
        # Iteramos sobre los diferente objetos
        for player in self.report.players:

            # SQL que usamos para actualizar la base de datos
            sql_player = """
                UPDATE statistics
                SET 
                    goals = goals + %(goals)s,
                    assists = assists + %(assists)s,
                    matches = matches + %(matches)s,
                    minutes = minutes + %(minutes)s,
                    yellow_card = yellow_card + %(yellow_card)s,
                    red_card = red_card + %(red_card)s
                WHERE id_player = %(id_player)s 
                RETURNING *;
                """

            # Estraemos los diferentes datos para agregarlos
            data_player = {
                "id_player" : player.id_player,
                "goals" : player.goals,
                "assists" : player.assists,
                "matches" : player.match,
                "minutes" : player.minutes_played,
                "yellow_card" : player.yellow_card,
                "red_card" : player.rd_card
            }

            # Intentamos actualizar la base de datos
            try: 
                self.db.cur.execute(sql_player, data_player)

            # Si no logra hacer el UPDATE 
            # entonces retorna el error
            except Exception as e:
                self.db.conn.rollback()
                print("Error:", e)

            # Si algun dato fue erroneo y la tabla 
            # no se actualizó entonces retorna un error
            if self.db.cur.rowcount == 0:
                raise ValueError("Statistics for player not found")
            
""""import os
import json
from pathlib import Path
from dotenv import load_dotenv

from db.initialize_db import DataBaseMCB
from db.table_statistics import StatidticsUpdateA
from agent.initialize_IA import ConnectBrain
from agent.valid_data_IA import MatchReport
from agent.actions_IA import GetQuery



# Cargamos el .env con la ruta absoluta
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Obtenemos la API KEY
api_key = os.getenv("API_KEY_OPENAI")

# Nos conectamos al cerebro de OpenAIS
brain = ConnectBrain(key=api_key).connect()

# El informe del partido
match_data = """
"""Resultado del partido: Real Madrid 2 : 0 Benfica
Mejor jugador del partido: hector (69d9c807-44de-46d6-9bc2-83fe33f49f6e)
equipo titular: hector (69d9c807-44de-46d6-9bc2-83fe33f49f6e), santiago (e2319e66-cd63-4863-9d69-0016e7390c50)
Eventos del partido: minuto 16 gol de hector, minuto 16 asistencia de santiago, minuto 34 gol de hector, minuto 34 asistencia de santiago.   
duracion del partido: 45 + 3 y 45 + 7
Estadisticas del partido: ..."""
"""

BASE_JSON = Path(__file__).resolve().parent / "config_IA.json"

# Cargamos las configuraciones del agente
with open(BASE_JSON, "r") as file:
    ia_config = json.load(file)
    ia_config["memory"].append({"role" : "user", "content" : match_data})

# Creamos el reporte
report = GetQuery(brain=brain, agent=ia_config, format=MatchReport).make_query()


# Iniciamos session en la base de datos
with DataBaseMCB() as db:

    # Actualizamos la base de datos
    StatisticsUpdateA(db=db, report=report).action()"""


# Clase que actualiza las estadisticas del jugador
# en la tabla statistics de manera manual
class StatisticsUpdateM:

    def __init__(self,db, id: UUID, attributes: str | int, colmn:str):
        # Una base de datos
        self.db = db
        # Id del jugador al cual queremos agregar alguna estadisitica
        self.id = id
        # Columna del jugador la cual queremos modificar
        self.colmn = colmn
        # Atributo por el cual queramos modificar
        self.attributes = attributes

    # Metodo cual actualiza la base de datos
    def action(self):
        # sql que usamos para actualizar la tabla
        sql = f"""
        UPDATE statistics
        SET {str(self.colmn)} = {str(self.colmn)} + %(attribute)s
        WHERE id_player = %(id)s
        RETURNING *;
        """

        # Datos para modificar la tabla
        data = {
            "attribute" : self.attributes,
            "id" : str(self.id)
        }

        # Intentamos actualizar la base de datos
        try: 
            self.db.cur.execute(sql, data)
                  
        # Si no logra hacer el UPDATE 
        # entonces retorna el error
        except Exception as e:
            self.db.conn.rollback()
            print("Error:", e)
        
        # Si algun dato fue erroneo y la tabla 
        # no se actualizó entonces retorna un error
        if self.db.cur.rowcount == 0:
            raise ValueError("Statistics for player not found")

"""
from uuid import UUID

from db.initialize_db import DataBaseMCB
from db.table_statistics import StatisticsUpdateM

with DataBaseMCB() as db:
    StatisticsUpdateM(db=db, id=UUID("69d9c807-44de-46d6-9bc2-83fe33f49f6e"), attributes=2, colmn="goals").action()
"""


# Retorna las Datos de la tabla statistics
# get_all() retorna una [()] con las filas de la base de datos
# get_by_colmn retorna una [()] con la columna de esa base de datos
# get_by_id retorna una () con la fila donde esta el id
# get_by_id y pasas column retorna una () con la columna del id deaseado
class StatisticSelect:

    # Columnas habiles en la base de datos
    ALLOWED_COLUMNS = {"goals", "assists", "matches", "minutes", "yellow_card", "red_card"}
    colmns = "goals, assists, matches, minutes, yellow_card, red_card"

    def __init__(self, db):
        # Base de datos a la que se conecta
        self.db = db

    # Retorna todos los datos de la base de datos
    def get_all(self):
        
        # creamos el sql
        sql = f"SELECT {self.colmns} FROM statistics"
        
        # Ejecuta el sql
        self.db.cur.execute(sql)

        # Retornamos los datos
        return self.db.cur.fetchall()

    # Retornamos todos los datos de una columna
    def get_by_colmn(self, colmn):
        # Validamos la columna que nos pasen
        if str(colmn) not in self.ALLOWED_COLUMNS:
                raise ValueError("Invalid column")
        # Creamos el sql
        sql = f"SELECT {str(colmn)} FROM statistics"

        # Ejecuta el sql
        self.db.cur.execute(sql)

        # Retornamos los datos
        return self.db.cur.fetchall()

    # Retorna la fila donde el id sea el deseado
    # y si le pasas una columna solo retorna la columna
    # donde esté ese id
    def get_by_id(self, id, colmn=None):
        # Si el usuario no puso el parametro colmn
        # entonces select pasa a ser todas las columnas de la bd
        if colmn == None:
            select = str(self.colmns)
        # Si pasa colmn, entonces se le atribuye el valor a select
        else:
            # Validar que colmn sea una columna valida de la base de datos
            if str(colmn) not in self.ALLOWED_COLUMNS:
                raise ValueError("Invalid column")
            
            select = f"{str(colmn)}"
        # Creamos el sql
        sql = f"""
                SELECT {str(select)}
                FROM statistics
                WHERE id_player = %(id)s
            """
        # preparamos el id
        data = {
            "id" : str(id)
            }
        
        # Ejecutamos el sql
        self.db.cur.execute(sql, data)
        # Retornamos los datos
        return self.db.cur.fetchall()
    
"""
from db.initialize_db import DataBaseMCB
from db.table_statistics import StatisticSelect

# Iniciamos session en la base de datos
with DataBaseMCB() as db:

    # Hacemos la prueba sobre los difeterentes esenarios
    print(StatisticSelect(db=db).get_all()) # retornamos todos los datos
    print(StatisticSelect(db=db).get_by_colmn(colmn="goals")) # retornamos todos los goles
    # retornamos la fila con id e2319e66-cd63-4863-9d69-0016e7390c50
    print(StatisticSelect(db=db).get_by_id(id="e2319e66-cd63-4863-9d69-0016e7390c50"))
    # retornamos los goles del jugador con el id e2319e66-cd63-4863-9d69-0016e7390c50
    print(StatisticSelect(db=db).get_by_id(id="e2319e66-cd63-4863-9d69-0016e7390c50", colmn="goals"))
"""