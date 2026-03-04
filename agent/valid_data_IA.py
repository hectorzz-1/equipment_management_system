from pydantic import BaseModel, Field
from typing import List

# Es la estructura y formato en que el 
# cerebro retornará los datos

# Las estadisticas de los jugadores en un diccionario
class PlayerStats(BaseModel):
    name: str
    id_player: str
    # ge=0 Valida que no retorne datos negativos
    goals: int = Field(default=0, ge=0)
    assists: int = Field(default=0, ge=0)
    yellow_card: int = Field(default=0, ge=0)
    rd_card: int = Field(default=0, ge=0)
    minutes_played: int = Field(default=0, ge=0)
    # Validar que no sea menor que 0 ni mayor que 1 
    match: int = Field(default=0, ge=0, li=1)

# Guradamos los judores en una lista
class MatchReport(BaseModel):
    players: List[PlayerStats]