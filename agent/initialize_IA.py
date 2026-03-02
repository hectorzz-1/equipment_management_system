from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv


# Clase que conecta con el cerebro de OpenAI
class ConnectBrain:

    # Le damos una clave API de openAI
    def __init__(self, key: str):
        self.key = key

    # Retornamos el cerebro de OpenAI
    def connect(self):
        return OpenAI(api_key=self.key)
    

if __name__ == "__main__":

    # Cargamos el .env con la ruta absoluta
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR / ".env")

    # Obtenemos la API KEY
    api_key = os.getenv("API_KEY_OPENAI")

    # Nos conectamos al cerebro de OpenAIS
    brain = ConnectBrain(key=api_key).connect()
    print(brain)