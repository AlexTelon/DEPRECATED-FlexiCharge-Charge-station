from enum import Enum, auto

class States(Enum):
    S_STARTUP = auto()
    S_AVAILABLE = auto()
    S_NOTAVAILABLE = auto()
    S_DISPLAYID = auto()
    S_PLUGINCABLE = auto()
    S_AUTHORIZING = auto()
    S_CONNECTINGTOCAR = auto()
    S_CONNECTED = auto()
    S_BUSY = auto()
    S_CHARGINGCANCELLED = auto()

class StateHandler:
    def __init__(self):
        self.__state = States.S_STARTUP

    def set_state(self, state):
        self.__state = state
        
    def get_state(self):
        return self.__state