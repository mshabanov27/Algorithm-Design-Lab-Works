import copy
from game_state import State


class MinimaxNode:
    def __init__(self, dice_roll, players, current_player_index, level, is_main_state=False):
        self.head = State(players, current_player_index)
        self.current_player_index = current_player_index % 4
        self.is_main_state = is_main_state
        self.dice_roll = dice_roll
        self.level = level
        self.children = []
        if self.level < 3:
            self.__define_child_states()

    def __define_child_states(self):
        next_player_index = (self.current_player_index + 1) % 4
        active_pieces = self.head.players[self.current_player_index].check_active_pieces(self.dice_roll)

        if self.is_main_state:
            for piece_index in range(len(active_pieces)):
                new_board = copy.deepcopy(self.head.players)
                new_board[self.current_player_index].check_active_pieces(self.dice_roll)[piece_index].move(self.dice_roll)
                self.children.append(MinimaxNode(self.dice_roll, new_board, next_player_index, self.level + 1))
            if self.dice_roll == 6 and self.head.players[self.current_player_index].check_inner_pieces:
                new_board = copy.deepcopy(self.head.players)
                unmoved = new_board[self.current_player_index].find_unmoved_piece()
                if unmoved is not None:
                    unmoved.take_out()
                    self.children.append(MinimaxNode(6, new_board, next_player_index, self.level + 1))
        else:
            for i in range(1, 7):
                for piece_index in range(len(active_pieces)):
                    new_board = copy.deepcopy(self.head.players)
                    new_board[self.current_player_index].check_active_pieces(self.dice_roll)[piece_index].move(self.dice_roll)
                    self.children.append(MinimaxNode(i, new_board, next_player_index, self.level + 1))
            if self.dice_roll == 6 and self.head.players[self.current_player_index].check_inner_pieces:
                new_board = copy.deepcopy(self.head.players)
                unmoved = new_board[self.current_player_index].find_unmoved_piece()
                if unmoved is not None:
                    unmoved.take_out()
                    self.children.append(MinimaxNode(6, new_board, next_player_index, self.level + 1))

    def find_best_solution(self):
        for level_1 in self.children:
            sum1 = 0
            for level_2 in level_1.children:
                sum2 = 0
                for level_3 in level_2.children:
                    sum2 += level_3.head.state_values[(self.current_player_index + 3) % 4]
                if len(level_2.children) != 0:
                    level_2.head.state_values[(self.current_player_index + 2) % 4] = sum2 / len(level_2.children)
                if level_2.head.state_values[(self.current_player_index + 2) % 4] is not None:
                    sum1 += level_2.head.state_values[(self.current_player_index + 2) % 4]
            if len(level_1.children) != 0:
                level_1.head.state_values[(self.current_player_index + 1) % 4] = sum1 / len(level_1.children)
        return self.__choose_max_state()

    def __choose_max_state(self):
        max_state = self.children[0]
        for child in self.children:
            if child.head.state_values[self.current_player_index] > max_state.head.state_values[self.current_player_index]:
                max_state = child
        self.check_kill(max_state)
        return max_state

    def check_kill(self, max_state):
        for player in max_state.head.players:
            if player != max_state.head.players[self.current_player_index]:
                for piece in player.pieces:
                    if piece.current_cell in max_state.head.players[self.current_player_index].define_player_cells():
                        piece.return_to_start()
