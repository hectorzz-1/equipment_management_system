import json
import os
from pathlib import Path
from dotenv import load_dotenv

from .initialize_IA import ConnectBrain
from .valid_data_IA import MatchReport

# Esta clase sirve para hacer un query al cerebro de Open AI
class GetQuery:

    # Como parametros recibe
    # brain = cerebro de Open AI
    # agent = un diccionario con las configuraciones del agente
    # format = Es el formato en que se van a mapear los datos
    def __init__(self,brain : str, agent:dict, format):
        self.brain = brain
        self.agent = agent
        self.format = format
    
    # Esta clase usa el cerebro de openIA para generar 
    # una estructura de datos ordenados
    def make_query(self):
        try:
            # Hacemos la query al cerebro de OpenAI
            response = self.brain.responses.parse(
                model=self.agent["model"],
                input=self.agent["memory"],
                temperature=self.agent["temperature"],
                max_output_tokens=self.agent["max_tokens"],
                text_format=self.format
            )

            # Retornamos los datos
            return response.output_parsed

        # Si algo sale mal entonces...
        except Exception as e:
            return {"error": str(e)}
        

if __name__ == "__main__":

    # Cargamos el .env con la ruta absoluta
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR / ".env")

    # Obtenemos la API KEY
    api_key = os.getenv("API_KEY_OPENAI")

    # Nos conectamos al cerebro de OpenAIS
    brain = ConnectBrain(key=api_key).connect()

    # El informe del partido
    match_data = """Resultado del partido: Real Madrid 2 : 0 Benfica
Mejor jugador del partido: Vinicius (uiidgh1234)
equipo titular: courtois (uiidqs7425), arnold (uidas7554), asensio (uiidqw6127), alaba (uiidkl7845), carreras (uiidvf7412), valverde (uiidqw6751), guler (uiidvb4567), messi (uiidrf7894), mbappe (uiidbv4554), Vinicius (uiidgh1234), rodrygo (uiidñs0821)
Eventos del partido: minuto 16 gol de Messi (uiidrf7894), minuto 16 asistencia de mbappe (uiidbv4554), minuto 34 gol de messi (uiidvb4567), minuto 34 asistencia de mbappe (uiidbv4554), minuto 57 asensio (uiidqw6127) recibió tarjeta amarilla, en el minuto 77 salió valverde (uiidqw6751) y entró mastantuono (uiidwz2587), minuto 79 alaba (uiidkl7845) recibió tarjeta roja, minuto 80 asensio (uiidqw6127) recibió roja despues de una doble amarilla.   
duracion del partido: 45 + 3 y 45 + 7
Estadisticas del partido: ..."""

    BASE_JSON = Path(__file__).resolve().parent / "config_IA.json"

    # Cargamos las configuraciones del agente
    with open(BASE_JSON, "r") as file:
        ia_config = json.load(file)
        ia_config["memory"].append({"role" : "user", "content" : match_data})

    # Hacemos la query
    report = GetQuery(brain=brain, agent=ia_config, format=MatchReport).make_query()
