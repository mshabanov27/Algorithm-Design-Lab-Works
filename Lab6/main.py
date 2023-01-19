import pygame
import csv
from random import random, randint
import copy
from cell import Cell
from player import Player
from minimax_tree import MinimaxNode


class GUI:
    def __init__(self):
        self.colors = ["red", "green", "yellow", "blue"]
        self.grid_size = 15
        self.screen = pygame.display.set_mode((765, 765))
        self.grid = self.get_grid()
        self.choice_made = True
        self.players = [Player(self.colors[x], self.grid) for x in range(0, 4)]
        self.winners = []
        pygame.init()
        self.screen.fill('black')
        self.launch_game_logic()

    def launch_game_logic(self):
        current_player_index = randint(0, 3)
        running = True
        key_pressed = True
        while running:
            self.draw_board()
            if key_pressed:
                current_player = self.players[current_player_index % 4]
                while current_player in self.winners:
                    self.draw_board()
                    current_player_index += 1
                    current_player = self.players[current_player_index % 4]
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    pygame.display.update()
                if self.choice_made:
                    dice_roll = randint(1, 6)
                self.players_move(current_player_index, current_player, dice_roll)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if self.choice_made:
                    current_player_index += 1
                    key_pressed = False
            else:
                self.draw_dice_result(dice_roll, current_player.colour)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            key_pressed = True

            pygame.display.update()

    def players_move(self, current_player_index, current_player, dice_roll):
        self.draw_dice_result(dice_roll, current_player.colour)
        active_pieces = current_player.check_active_pieces(dice_roll)
        if dice_roll == 6:
            if len(active_pieces) > 0:
                if current_player_index % 4 == 0:
                    self.choice_made = self.check_user_choice(current_player, active_pieces, dice_roll)
                else:
                    self.ai_choice(dice_roll, current_player_index % 4)
            else:
                unmoved = current_player.find_unmoved_piece()
                if unmoved is not None:
                    unmoved.take_out()
        else:
            if len(active_pieces) == 1:
                piece_index = self.find_out_piece(current_player)
                current_player.pieces[piece_index].move(dice_roll)
                if current_player.pieces[piece_index].is_home():
                    current_player.pieces.remove(current_player.pieces[piece_index])
            elif len(active_pieces) > 1:
                if current_player_index % 4 == 0:
                    self.choice_made = self.check_user_choice(current_player, active_pieces, dice_roll)
                else:
                    self.ai_choice(dice_roll, current_player_index % 4)
        if not current_player.pieces:
            self.winners.append(current_player)
            self.players.remove(current_player)
        self.check_kill(current_player)

    def check_user_choice(self, current_player, active_pieces, dice_roll):
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
            click = self.check_pieces(current_player, active_pieces, dice_roll)
            if click[0] and click[1] in active_pieces:
                click[1].move(dice_roll)
                if click[1].is_home():
                    current_player.pieces.remove(click[1])
                return True
            elif click[0] and click[1] not in active_pieces:
                click[1].take_out()
                return True
        return False

    def draw_board(self):
        self.get_grid()
        for player in self.players:
            for piece in player.pieces:
                piece.draw(self.screen, player.colour)
        self.display_winners()

    def draw_dice_result(self, dice_roll, color):
        pygame.draw.rect(self.screen, color, pygame.Rect((305, 305), (154, 154)), 20)
        dice_font = pygame.font.SysFont("monospace", 80, True)
        dice_result = dice_font.render(f"{dice_roll}", True, color)
        self.screen.blit(dice_result, (355, 340))

    def get_grid(self):
        grid = [list([] for x in range(0, self.grid_size)) for y in range(0, self.grid_size)]

        colours = list(csv.reader(open("colour.csv")))

        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                grid[x][y] = Cell(x, y, colours[y][x])
                grid[x][y].draw(self.screen)

        return grid

    @staticmethod
    def find_out_piece(current_player):
        for i in range(len(current_player.pieces)):
            if current_player.pieces[i].is_out():
                return i

    def check_pieces(self, current_player, active_pieces, dice_roll):
        if dice_roll == 6:
            for piece in (active_pieces + current_player.check_inner_pieces()):
                mouse = pygame.mouse.get_pos()
                if mouse[0] // 51 == piece.current_cell.x and mouse[1] // 51 == piece.current_cell.y:
                    return True, piece
            return False, None
        else:
            for piece in active_pieces:
                mouse = pygame.mouse.get_pos()
                if mouse[0] // 51 == piece.current_cell.x and mouse[1] // 51 == piece.current_cell.y:
                    return True, piece
            return False, None

    def check_kill(self, current_player):
        for player in self.players:
            if player != current_player:
                for piece in player.pieces:
                    if piece.current_cell in current_player.define_player_cells():
                        piece.return_to_start()

    def ai_choice(self, dice_roll, current_player_index):
        tree = MinimaxNode(dice_roll, copy.deepcopy(self.players), current_player_index, 0, True)
        solution = tree.find_best_solution()
        self.players = solution.head.players

    def display_winners(self):
        font = pygame.font.SysFont("monospace", 30, True)
        for i in range(len(self.winners)):
            coordinates = self.winners[i].coordinates
            pygame.draw.rect(self.screen, 'white', pygame.Rect(coordinates, (204, 204)))
            winner_sign = font.render(f"Winner #{(i + 1) % 4}", True, self.winners[i].colour)
            self.screen.blit(winner_sign, (coordinates[0] + 20, coordinates[1] + 80))

    # def check_homes(self):
    #     for player in self.players:
    #         for piece in player.pieces:
    #             if piece.is_home():
    #                 player.pieces.remove(piece)

ludo = GUI()
