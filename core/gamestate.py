from enum import Enum,auto

class GameState(Enum):
    START = auto()
    INSTR = auto()
    PLAY = auto()
    CLEAR = auto()
    GAMEOVER = auto()