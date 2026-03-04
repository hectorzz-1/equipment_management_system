from dataclasses import dataclass, asdict
from uuid import uuid4, UUID
from abc import ABC, abstractmethod

from .initialize_db import DataBaseMCB

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
        

# Clase padre de las clases que
# van a controlar las acciones de
# la tabla player.
class PlayerController(ABC):
    
    # Metodo que haga la determinada acción en la bd
    @abstractmethod
    def action(self):
        pass


class PlayerInsert(PlayerController):
    
    insert = """
        INSERT INTO players (id, name, last_name, number)
        VALUES (%(id)s, %(name)s, %(last_name)s, %(number)s)
        """

    def __init__(self, db, data):
        # Pasar la base de datos
        self.db = db
        # Pasar los datos que se insertarán
        self.data = data

    # Inserta un jugador nuevo en la base de datos
    def action(self):

        # Pasamos el id de tipo UUID a tipo str
        # para que la base de datos lo pueda manejar
        if isinstance(self.data.id, UUID):
            self.data.id = str(self.data.id)
        
        # Intenta hacer un insert
        # en la tabla players
        try: 
            self.db.cur.execute(
                self.insert, # sql
                asdict(self.data) # volvemos el objeto un diccionario
            )
        
        # Si no logra hacer el insert 
        # entonces retorna el error
        except Exception as e:
            self.db.conn.rollback()
            print("Error:", e)


# Clase que actualiza datos del jugador
# en la tabla players
class PlayerUpdate(PlayerController):

    def __init__(self,db, id: UUID, attributes: str | int, colmn:str):
        # Una base de datos
        self.db = db
        # Id del jugador al cual queremos cambiar algun dato
        self.id = id
        # Columna del jugador la cual queremos modificar
        self.colmn = colmn
        # Atributo por el cual queramos modificar
        self.attributes = attributes

    # Metodo cual actualiza la base de datos
    def action(self):
        # sql que usamos para actualizar la tabla
        sql = f"""
        UPDATE players
        SET {str(self.colmn)} = %(attribute)s
        WHERE id = %(id)s
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
            raise ValueError("Player data not found")
        

if __name__ == "__main__":

    # nos conectamos a la base de datos
    with DataBaseMCB() as db:
        # creamos un jugador
        hector = Player(name="santiago", last_name="sanabria mendez", id=uuid4(), number=6)

        # Insertamos al jugador
        PlayerInsert(db=db, data=hector).action()

        # Actualizamos una columna de un jugador
        PlayerUpdate(db=db, id=UUID("69d9c807-44de-46d6-9bc2-83fe33f49f6e"), attributes=7, colmn="number").action()

        