import pygame
from MazeGenerator import Maze
from BFS import GraphForBFS
from A_Star import GraphForAStar
from FileWorker import FileWorker

# User Interface class


class UI:
    def __init__(self):
        self.__image_index = 1
        self.__square_size = 40
        self.__width = 1800
        self.__height = 1000
        self.__cols = 35
        self.__rows = 23
        self.__running = True
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__maze_object = Maze(1, 1, self.__cols, self.__rows)
        self.__grid = self.__maze_object.grid
        self.__dead_ends = None
        self.__pos_left = None
        self.__pos_right = None
        self.__used_algorithm = None
        self.__algorithm_worked = False
        self.__path = None
        self.__visited = None
        self.__algorithm_received = False
        self.__path_limiter = 0
        self.__path_found = True
        self.__initializator()

    def __initializator(self):
        pygame.init()
        pygame.display.set_caption("Labyrinth")
        self.__intro_menu()

    def __intro_menu(self):
        while self.__running:
            self.__screen.fill('white')
            pygame.draw.rect(self.__screen, 'black', [550, 230, 750, 150])
            pygame.draw.rect(self.__screen, 'black', [550, 500, 750, 150])
            font = pygame.font.SysFont('Times New Roman', 70)
            textStart = font.render('Згенерувати лабіринт', True, 'white')
            textExit = font.render('Вийти', True, 'white')
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 550 <= mouse[0] <= 1400 and 230 <= mouse[1] <= 370:
                        self.__runner()
                    if 550 <= mouse[0] <= 1400 and 500 <= mouse[1] <= 650:
                        self.__running = False
            self.__screen.blit(textStart, (600, 260))
            self.__screen.blit(textExit, (825, 530))
            pygame.display.update()

    def __runner(self):
        while self.__running:
            self.__screen.fill('white')
            self.__draw_buttons()

            [[pygame.draw.rect(self.__screen, pygame.Color('black'), self.__get_square(x, y))
              for x, col in enumerate(row) if col] for y, row in enumerate(self.__grid)]

            if self.__pos_left is not None:
                pygame.draw.rect(self.__screen, 'limegreen',
                                 self.__get_square_in_decarte(self.__pos_left[0], self.__pos_left[1]))
            if self.__pos_right is not None:
                pygame.draw.rect(self.__screen, 'brown3',
                                 self.__get_square_in_decarte(self.__pos_right[0], self.__pos_right[1]))

            if self.__pos_left is not None and self.__pos_right is not None:
                if not self.__algorithm_received:
                    self.__used_algorithm = self.__check_press()
                    if self.__used_algorithm is not None:
                        self.__algorithm_received = True
                if self.__used_algorithm is not None:
                    self.__draw_path_and_visited()
                    self.__path_limiter += 1
            self.__check_press()
            pygame.display.update()

    def __check_press(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.__pos_left is None:
                self.__pos_left = pygame.mouse.get_pos()
                if self.__pos_left[0] > 1400 or self.__pos_left[1] > 920:
                    self.__pos_left = None
                else:
                    leftSquare = self.__get_matrix_index(self.__pos_left[0], self.__pos_left[1])
                    if self.__grid[leftSquare[1]][leftSquare[0]] == 1:
                        self.__pos_left = None
                    if self.__pos_right is not None and leftSquare == self.__get_matrix_index(self.__pos_right[0],
                                                                                              self.__pos_right[1]):
                        self.__pos_left = None
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3 and self.__pos_right is None:
                self.__pos_right = pygame.mouse.get_pos()
                if self.__pos_right[0] > 1400 or self.__pos_right[1] > 920:
                    self.__pos_right = None
                else:
                    rightSquare = self.__get_matrix_index(self.__pos_right[0], self.__pos_right[1])
                    if self.__grid[rightSquare[1]][rightSquare[0]] == 1:
                        self.__pos_right = None
                    if self.__pos_left is not None and rightSquare == self.__get_matrix_index(self.__pos_left[0],
                                                                                              self.__pos_left[1]):
                        self.__pos_right = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.__pos_left is not None and self.__pos_right is not None:
                    if 1450 <= mouse[0] <= 1750 and 50 <= mouse[1] <= 150:
                        return 'BFS'
                    if 1450 <= mouse[0] <= 1750 and 200 <= mouse[1] <= 300:
                        return 'astarEuclidean'
                if 1450 <= mouse[0] <= 1750 and 350 <= mouse[1] <= 450:
                    self.__grid = FileWorker.read_grid('maze.txt')
                    self.__pos_left = None
                    self.__pos_right = None
                    self.__used_algorithm = None
                    self.__algorithm_worked = False
                    self.__path = None
                    self.__visited = None
                    self.__algorithm_received = False
                    self.__path_limiter = 0
                    self.__path_found = True
                if 1450 <= mouse[0] <= 1750 and 470 <= mouse[1] <= 570:
                    self.__pos_left = None
                    self.__pos_right = None
                    self.__used_algorithm = None
                    self.__algorithm_worked = False
                    self.__path = None
                    self.__visited = None
                    self.__algorithm_received = False
                    self.__path_limiter = 0
                    self.__path_found = True
                if 1450 <= mouse[0] <= 1750 and 590 <= mouse[1] <= 690:
                    self.__pos_left = None
                    self.__pos_right = None
                    self.__used_algorithm = None
                    self.__algorithm_worked = False
                    self.__path = None
                    self.__visited = None
                    self.__algorithm_received = False
                    self.__path_limiter = 0
                    self.__path_found = True
                    self.__grid = Maze(1, 1, self.__cols, self.__rows).grid
                if 1450 <= mouse[0] <= 1750 and 710 <= mouse[1] <= 810:
                    FileWorker.write_grid('maze.txt', self.__grid)
                if 1450 <= mouse[0] <= 1750 and 830 <= mouse[1] <= 890:
                    self.__running = False

    def __get_square_in_decarte(self, posX, posY):
        square = self.__square_size
        return posX // square * square + 1, posY // square * square + 1, square, square

    def __get_matrix_index(self, x, y):
        i = x // self.__square_size
        j = y // self.__square_size
        return i, j

    def __get_circle(self, x, y):
        return (x * self.__square_size + self.__square_size // 2,
                y * self.__square_size + self.__square_size // 2), self.__square_size // 4

    def __get_square(self, x, y):
        return x * self.__square_size + 1, y * self.__square_size + 1, self.__square_size, self.__square_size

    def __draw_path_and_visited(self):
        start = (self.__pos_left[1] // self.__square_size, self.__pos_left[0] // self.__square_size)
        end = (self.__pos_right[1] // self.__square_size, self.__pos_right[0] // self.__square_size)
        if self.__used_algorithm == 'BFS' and not self.__algorithm_worked:
            self.__algorithm_worked = True
            search = GraphForBFS(self.__grid)
            self.__dead_ends = search.dead_ends
            self.__path, self.__visited = search.BFS(start, end)
            if self.__path == -1:
                self.__path_found = False
                self.__path = None
                self.__visited = None

        if self.__used_algorithm == 'astarEuclidean' and not self.__algorithm_worked:
            self.__algorithm_worked = True
            astarEuclidean = GraphForAStar(self.__grid)
            self.__dead_ends = astarEuclidean.dead_ends
            self.__path, self.__visited = astarEuclidean.AStarAlgorithm(start, end, GraphForAStar.euclidHeuristic)
            if self.__path == -1:
                self.__path_found = False
                self.__path = None
                self.__visited = None

        if self.__used_algorithm is not None and self.__path_found:
            for tile in self.__visited:
                pygame.draw.rect(self.__screen, pygame.Color('lemonchiffon'), self.__get_square(tile[1][1], tile[1][0]))

            i = self.__path_limiter
            if i > len(self.__path):
                self.__path_limiter = len(self.__path)
            for line in range(1, i - 1):
                pygame.draw.circle(self.__screen, pygame.Color('blueviolet'),
                                   self.__get_circle(self.__path[line][1][1], self.__path[line][1][0])[0],
                                   self.__get_circle(self.__path[line][1][1], self.__path[line][1][0])[1])

            if self.__path_limiter < len(self.__path):
                pygame.draw.rect(self.__screen, pygame.Color('brown3'), self.__get_square(self.__path[i][1][1], self.__path[i][1][0]))

            pygame.draw.rect(self.__screen, 'limegreen',
                             self.__get_square_in_decarte(self.__pos_left[0], self.__pos_left[1]))
            pygame.draw.rect(self.__screen, 'brown3',
                             self.__get_square_in_decarte(self.__pos_right[0], self.__pos_right[1]))
            self.__show_stats(self.__visited, self.__path)

    def __draw_buttons(self):
        self.__create_sign('Оберіть алгоритм:', (1450, 0), 40)
        self.__create_sign('Опції:', (1547, 300), 40)
        self.__create_button('Алгоритм BFS', [1450, 50, 300, 100], (1500, 80), 30)
        self.__create_button('Алгоритм A*', [1450, 190, 300, 100], (1520, 200), 30)
        self.__create_button('(евклідова евристика)', [0, 0, 0, 0], (1495, 240), 22)
        self.__create_button('Завантажити з файлу', [1450, 350, 300, 100], (1465, 380), 30)
        self.__create_button('Очистити шлях', [1450, 470, 300, 100], (1500, 500), 30)
        self.__create_button('Згенерувати новий', [1450, 590, 300, 100], (1480, 600), 30)
        self.__create_button('лабіринт', [0, 0, 0, 0], (1547, 640), 30)
        self.__create_button('Зберегти результат', [1450, 710, 300, 100], (1480, 720), 30)
        self.__create_button('роботи', [0, 0, 0, 0], (1547, 760), 30)
        self.__create_button('Вийти', [1450, 830, 300, 60], (1555, 840), 30)
        if not self.__algorithm_received and self.__path_found:
            self.__create_sign('ЛКМ - задати стартову клітину, ПКМ - задати кінцеву клітину', (10, 940), 30)
        elif not self.__path_found:
            self.__create_sign('Шлях відсутній', (10, 940), 30)

    def __create_button(self, text, button_size, place, font_size):
        pygame.draw.rect(self.__screen, 'black', button_size)
        font = pygame.font.SysFont('Times New Roman', font_size)
        button = font.render(text, True, 'white')
        self.__screen.blit(button, place)

    def __create_sign(self, text, place, font_size):
        font = pygame.font.SysFont('Times New Roman', font_size)
        sign = font.render(text, True, 'black')
        self.__screen.blit(sign, place)

    def __show_stats(self, visited, path):
        font = pygame.font.SysFont('Times New Roman', 30)

        visitedNodes = f'Всього станів: {len(set(visited))}; '
        allNodes = f"Всього станів у пам'яті: {self.__graph_size()}; "
        deadEndsCount = f'Кількість глухих кутів: {self.__dead_ends} '
        pathLength = f'Довжина шляху: {len(path) - 1}; '
        allStats = visitedNodes + allNodes + deadEndsCount + pathLength
        stats = font.render(allStats, True, 'black')
        self.__screen.blit(stats, (10, 940))

    def __graph_size(self):
        size = 0
        for line in self.__grid:
            for tile in line:
                if tile == 0:
                    size += 1
        return size

