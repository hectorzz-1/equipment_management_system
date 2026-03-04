import os
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
Resultado del partido: Real Madrid 2 : 0 Benfica
Mejor jugador del partido: hector (69d9c807-44de-46d6-9bc2-83fe33f49f6e)
equipo titular: hector (69d9c807-44de-46d6-9bc2-83fe33f49f6e), santiago (e2319e66-cd63-4863-9d69-0016e7390c50)
Eventos del partido: minuto 16 gol de hector, minuto 16 asistencia de santiago, minuto 34 gol de hector, minuto 34 asistencia de santiago.   
duracion del partido: 45 + 3 y 45 + 7
Estadisticas del partido: ...
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
    StatidticsUpdateA(db=db, report=report).action()
