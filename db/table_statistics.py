from dataclasses import dataclass
from uuid import UUID                 
from initialize_db import DataBaseMCB 
from dataclasses import asdict        


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



if __name__ == "__main__":
    # nos conectamos a la base de datos
    with DataBaseMCB() as db:
        # inicializamos las estadsticas de un jugador
        hector_statistics = Statistics(id_player=UUID("e2319e66-cd63-4863-9d69-0016e7390c50"))

        # Insertamos las estadisticas a la base de datos
        StatisticsAction(db=db, data=hector_statistics, sql=StatisticSQL).insert()