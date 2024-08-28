import map
import player
import logging

class GameStateManager:
    def __init__(self):
        self.gamestate = GameState()

class GameState:
    def __init__(self):
        self.map = map.Map()
        self.player = player.Player()
        self.round_phase = ''

    def update_round_phase(self, phase):
        self.round_phase = phase
        logging.info('Round phase: ' + phase)

    def update_round_kills(self, kills):
        if self.player.state.round_kills != kills and kills != 0:
            self.player.state.round_kills = kills
            #print(self.player.name + ' got a kill.')
