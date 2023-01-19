import pygame


class Cell:

    def __init__(self, x, y, colour_id, cell_size=50, border_size=1):
        self.x = x
        self.y = y
        self.colour_id = int(colour_id)
        self.cell_size = cell_size
        self.border_size = border_size

    def __str__(self):
        return f'{self.x} / {self.y} / {self.colour()}'

    def colour(self):
        if self.colour_id == 0:
            return pygame.Color("white")
        elif self.colour_id == 1:
            return pygame.Color("darkred")
        elif self.colour_id == 2:
            return pygame.Color("darkgreen")
        elif self.colour_id == 3:
            return pygame.Color("darkblue")
        elif self.colour_id == 4:
            return pygame.Color("orange")
        else:
            return pygame.Color("black")

    def position(self, offset=0):
        x = (self.x * (self.cell_size + self.border_size)) + offset
        y = (self.y * (self.cell_size + self.border_size)) + offset

        return x, y

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour(), pygame.Rect(self.position(), (self.cell_size, self.cell_size)))


