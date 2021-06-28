from enum import Enum 
class AntState(Enum):
    SEARCHING_PATH = 1
    RETURNING = 2
    IDLE = 3