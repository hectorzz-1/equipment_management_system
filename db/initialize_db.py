from dotenv import load_dotenv
from pathlib import Path
import os
import psycopg2 as ps2

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# Esto crea una conexion con la db
# y la cierra cuando se deje de usar
# la conexión
# se usa con with ... as ... :   
class DataBaseMCB:

    # Abre una conexion y crea un cursor
    # retorna self
    # de manera que tendremos acceso a conn y cur
    def __enter__(self):
        # Conexión
        self.conn = ps2.connect(
            host = os.getenv("DB_HOST"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT"),
        )
        # Cursor
        self.cur = self.conn.cursor()
        return self

    # Cierra la conexión de conn y curr 
    def __exit__(self, exc_type, exc, tb):
        # Antes de cerrar la conexión hace un commit
        # solo si no hay errores. 
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
            
        # conexión
        self.conn.close()
        # cursor
        self.cur.close()


if __name__ == "__main__":

    with DataBaseMCB() as db:
        print("hola")