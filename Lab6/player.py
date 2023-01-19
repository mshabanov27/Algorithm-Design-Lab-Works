from piece import Piece


class Player:
    def __init__(self, colour, grid):
        self.colour = colour
        self.grid = grid
        self.start_cells = self.indicate_start_cells()
        self.pieces = [Piece(self.colour, self.start_cells[i], grid) for i in range(0, 4)]
        self.coordinates = self.define_coordinates()

    def check_active_pieces(self, move_length):
        active = []
        for piece in self.pieces:
            if piece.position != -1 and piece.position + move_length <= piece.home_position:
                active.append(piece)
        return active

    def check_moving_pieces(self, move_length):
        moving = []
        for piece in self.pieces:
            if piece.position + move_length <= piece.home_position:
                moving.append(piece)
        return moving

    def check_inner_pieces(self):
        inner = []
        for piece in self.pieces:
            if piece.is_in():
                inner.append(piece)
        return inner

    def indicate_start_cells(self):
        if self.colour == 'red':
            return [self.grid[1][1], self.grid[1][4], self.grid[4][1], self.grid[4][4]]
        elif self.colour == 'blue':
            return [self.grid[1][10], self.grid[1][13], self.grid[4][10], self.grid[4][13]]
        elif self.colour == 'green':
            return [self.grid[10][1], self.grid[10][4], self.grid[13][1], self.grid[13][4]]
        else:
            return [self.grid[10][10], self.grid[10][13], self.grid[13][10], self.grid[13][13]]

    def define_player_cells(self):
        cells = []
        for piece in self.pieces:
            cells.append(piece.current_cell)
        return cells

    def find_unmoved_piece(self):
        for piece in self.pieces:
            if piece.is_in():
                return piece

    def define_coordinates(self):
        if self.colour == 'red':
            return 50, 50
        elif self.colour == 'blue':
            return 50, 510
        elif self.colour == 'green':
            return 510, 50
        else:
            return 510, 510

