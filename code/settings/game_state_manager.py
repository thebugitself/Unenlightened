class GameState: #penerapan enkapsulasi
    def __init__(self, currentState):
        self.__currentState = currentState
    
    def get_state(self):
        return self.__currentState
    
    def set_state(self, state):
        self.__currentState = state