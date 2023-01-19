class State:
    def __init__(self, players, current_player_index):
        self.players = players
        self.current_player_index = current_player_index
        self.state_values = self.count_state_values()

    def count_state_values(self):
        state_values = []
        for i in range(len(self.players)):
            state_values.append(self.get_state_value(self.players[i]))
        return state_values

    def get_state_value(self, player):
        value = 0
        for piece in player.pieces:
            if piece.is_out():
                value += 1
            if piece.is_home():
                value += 2
        value += self.check_kills() * 3
        return value

    def check_kills(self):
        kills = 0
        current_player = self.players[self.current_player_index]
        for player in self.players:
            if player != current_player:
                for piece in player.pieces:
                    if piece.current_cell in current_player.define_player_cells():
                        kills += 1
        return kills
