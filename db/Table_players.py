from dataclasses import dataclass
from uuid import uuid4, UUID
from initialize_db import DataBaseMCB
from dataclasses import asdict

# Esta clase retorna un objeto
# al cual podremos consultar los diferentes datos
# ejemplo Player.name y accedemos al nombre
# o player = Player(...) y abstraemos el objeto con todos los datos
@dataclass
class Player:
    # id del jugador
    id: UUID
    # nombre del jugador
    name: str
    # apellido del jugador
    last_name: str
    # numero que usa el jugador
    number: int

    # Valida los datos
    def __post_init__(self):

        # Valida que name sea str
        if isinstance(self.name, str):
            raise ValueError("name must be string")
        # Valida que el name no esté vacío
        if not self.name.strip():
            raise ValueError("name cannot be empty")
        # Validar que name tenga menos de 50 caractéres
        if len(self.name) >= 50:
            raise ValueError("name is very long")
        
        # Valida que last_name sea str
        if isinstance(self.last_name, str):
            raise ValueError("last_name must be string")
        # Valida que el last_name no esté vacío
        if not self.last_name.strip():
            raise ValueError("last_name cannot be empty")
        # Validar que last_name tenga menos de 50 caractéres
        if len(self.last_name) >= 50:
            raise ValueError("last_name is very long")
        
        # Valida si number es un int
        if isinstance(self.number, int):
            raise ValueError("number must be integer")
        # Valida que number no sea menor que 1
        if self.number <= 0:
            raise ValueError("number must be greater than 0")
        # Validar que number sea menor que 100
        if self.number >= 100:
            raise ValueError("number must not be greater than 100")
        

# Esta clase contendrá el lenguaje sql
# que se usará para la tabla players
class PlayerSQL:

    # SQL que sirve para hacer un insert en la tabla players
    insert = """
        INSERT INTO players (id, name, last_name, number)
        VALUES (%(id)s, %(name)s, %(last_name)s, %(number)s)
        """
    

# Gestiona la tabla players
# inserta
# elimina
# retorna
class PlayersAction:
    
    def __init__(self, db, data, sql: PlayerSQL):
        # Pasar la base de datos
        self.db = db
        # Pasar los datos que se insertarán
        self.data = data
        # Pasar la clase PlayersSQL para disponer del lenguaje SQL
        self.sql = sql

    # Inserta un jugador nuevo en la base de datos
    def insert(self):

        # Pasamos el id de tipo UUID a tipo str
        # para que la base de datos lo pueda manejar
        if isinstance(self.data.id, UUID):
            self.data.id = str(self.data.id)
        
        # Intenta hacer un insert
        # en la tabla players
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
        # creamos un jugador
        hector = Player(name="santiago", last_name="sanabria mendez", id=uuid4(), number=6)

        # Insertamos al jugador
        PlayersAction(db=db, data=hector, sql=PlayerSQL).insert()