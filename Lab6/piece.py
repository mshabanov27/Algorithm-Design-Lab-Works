import pygame


class Piece:
    def __init__(self, colour, start_cell, grid):
        self.position = -1
        self.home_position = 56
        self.colour = colour
        self.grid = grid
        self.start = start_cell
        self.current_cell = start_cell

    def take_out(self):
        self.position = 0
        self.current_cell = self.define_first_cell()

    def move(self, places):
        if self.can_move(places):
            self.position += places
            for i in range(places):
                self.current_cell = self.move_one_step()

    def draw(self, screen, colour):
        if self.current_cell is not None:
            pygame.draw.circle(screen, colour, self.current_cell.position(25), 23)
            pygame.draw.circle(screen, pygame.Color("black"), self.current_cell.position(25), 23, 4)

    def can_move(self, places):
        if (self.position + places) <= self.home_position:
            return True
        return False

    def moves_left(self):
        return self.home_position - self.position

    def is_in(self):
        if self.position == -1:
            return True
        return False

    def is_out(self):
        if self.position > -1 and not self.is_home():
            return True
        return False

    def is_home(self):
        if self.position == self.home_position:
            return True
        return False

    def return_to_start(self):
        if not self.is_home():
            self.position = -1
            self.current_cell = self.start

    def define_first_cell(self):
        if self.colour == 'red':
            return self.grid[1][6]
        elif self.colour == 'blue':
            return self.grid[6][13]
        elif self.colour == 'green':
            return self.grid[8][1]
        else:
            return self.grid[13][8]

    def move_one_step(self):
        x = self.current_cell.y
        y = self.current_cell.x
        if (x == 6 and y == 5) or (x == 8 and y == 9):
            return self.grid[x][y]
        elif x == 5 and y == 8:
            return self.grid[y + 1][x + 1]
        elif x == 9 and y == 6:
            return self.grid[y - 1][x - 1]

        if x == 6 and (0 <= y <= 4 or 9 <= y <= 13) or (x == 0 and y == 6):
            return self.grid[y + 1][x]
        elif x == 8 and (1 <= y <= 5 or 10 <= y <= 14) or (x == 14 and y == 8):
            return self.grid[y - 1][x]
        elif y == 6 and (1 <= x <= 5 or 10 <= x <= 14) or (y == 0 and x == 8):
            return self.grid[y][x - 1]
        elif y == 8 and (0 <= x <= 4 or 9 <= x <= 13) or (y == 14 and x == 6):
            return self.grid[y][x + 1]
        else:
            return self.check_home_entrance(x, y)

    def check_home_entrance(self, x, y):
        if x == 7 and 0 <= y <= 5:
            if self.colour == 'red':
                return self.grid[y + 1][x]
            else:
                return self.grid[y][x - 1]
        elif y == 7 and 9 <= x <= 14:
            if self.colour == 'blue':
                return self.grid[y][x - 1]
            else:
                return self.grid[y - 1][x]
        elif y == 7 and 0 <= x <= 5:
            if self.colour == 'green':
                return self.grid[y][x + 1]
            else:
                return self.grid[y + 1][x]
        elif x == 7 and 9 <= y <= 14:
            if self.colour == 'yellow':
                return self.grid[y - 1][x]
            else:
                return self.grid[y][x + 1]
