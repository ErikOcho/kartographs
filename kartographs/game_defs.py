from enum import Enum
from dataclasses import dataclass


# Definícia fáz hry.
class GamePhase(Enum):
    JAR = 1
    LETO = 2
    JESEN = 3
    ZIMA = 4


# Definícia typov kariet.
class CardType(Enum):
    SEARCH = 1
    BEAST = 2
    TEMPLE = 3


# Definícia karty.
@dataclass
class Card():
    """Card class."""
    value: int
    image: str
    type: CardType = CardType.SEARCH


# Slovník prekladu fáz hry.
game_phase_dict = {
    GamePhase.JAR: "JAR",
    GamePhase.LETO: "LETO",
    GamePhase.JESEN: "JESEN",
    GamePhase.ZIMA: "ZIMA"
}
