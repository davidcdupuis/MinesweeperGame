from __future__ import print_function
import numpy as np
import pygame
import random
from settings import *

''' Class Tile:

    Properties: value = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
                revealed = True/false
'''
class Tile:
    def __init__(self, val = 0, prob = None):
        self.value = val
        self.revealed = False
        self.flagged = False
        self.questioned = False
        self.probability = prob # holds probability of mine being in tile
        self.row = 0
        self.column = 0

    ''' Function to manage tile drawing onto screen
    '''
    def draw(self, screen, x, y, prob = False):
        if self.revealed:
            if self.value == 9:
                #screen.blit(MINE, [x, y, w, h])
                font = pygame.font.SysFont(FONT, TILETEXT, True, False)
                text = font.render('X', True, BLACK)
                pygame.draw.rect(screen, (255, 153, 153), [x, y, WIDTH, HEIGHT])
                pygame.draw.rect(screen, (255, 51, 51), [x, y, WIDTH, HEIGHT], 2)
                pygame.draw.rect(screen, (255, 0, 0), [x, y, WIDTH, HEIGHT], 1)
                screen.blit(text, [x+ 5, y, WIDTH, HEIGHT])
            else:
                # draw cell with value
                # screen.blit(PRESSED, [x, y, w, h])
                font = pygame.font.SysFont(FONT, TILETEXT, True, False)
                text = font.render(str(self.value), True, BLACK)
                pygame.draw.rect(screen, (0, 204, 0), [x, y, WIDTH, HEIGHT])
                pygame.draw.rect(screen, DARKGREY, [x, y, WIDTH, HEIGHT], 2)
                pygame.draw.rect(screen, DARKERGREY, [x, y, WIDTH, HEIGHT], 1)
                screen.blit(text, [x + 5, y, WIDTH, HEIGHT])
        elif self.flagged:
            font = pygame.font.SysFont(FONT, TILETEXT, True, False)
            text = font.render('!', True, BLACK)
            pygame.draw.rect(screen, GREY, [x, y, WIDTH, HEIGHT])
            pygame.draw.rect(screen, DARKGREY, [x, y, WIDTH, HEIGHT], 2)
            pygame.draw.rect(screen, DARKERGREY, [x, y, WIDTH, HEIGHT], 1)
            screen.blit(text, [x + 5, y, WIDTH, HEIGHT])
        elif self.questioned:
            font = pygame.font.SysFont(FONT, TILETEXT, True, False)
            text = font.render('?', True, BLACK)
            pygame.draw.rect(screen, GREY, [x, y, WIDTH, HEIGHT])
            pygame.draw.rect(screen, DARKGREY, [x, y, WIDTH, HEIGHT], 2)
            pygame.draw.rect(screen, DARKERGREY, [x, y, WIDTH, HEIGHT], 1)
            screen.blit(text, [x + 5, y, WIDTH, HEIGHT])
        else:
            if prob:
                font = pygame.font.SysFont(FONT, 30, True, False)
                text = font.render('{0}%'.format((self.probability, '-')[not self.probability]), True, BLACK)
                pygame.draw.rect(screen, GREY, [x, y, WIDTH, HEIGHT])
                pygame.draw.rect(screen, DARKGREY, [x, y, WIDTH, HEIGHT], 2)
                pygame.draw.rect(screen, DARKERGREY, [x, y, WIDTH, HEIGHT], 1)
                screen.blit(text, [x + 2, y + 10, WIDTH, HEIGHT])
            else:
                pygame.draw.rect(screen, GREY, [x, y, WIDTH, HEIGHT])
                pygame.draw.rect(screen, DARKGREY, [x, y, WIDTH, HEIGHT], 2)
                pygame.draw.rect(screen, DARKERGREY, [x, y, WIDTH, HEIGHT], 1)

    def __str__(self):
        return "[ {0} ]".format(self.value)

''' Class board
    Will hold all the information of the minesweeper board
'''
class Board:
    def __init__(self, width, height, mines = None):
        # we need to fill the minesweeper board with tile objects
        self.board = [[Tile(0) for j in range(width)] for i in range(height)]
        self.width = width
        self.height = height
        self.helperProb = False
        self.mines = None
        self.tiles = width * height
        if mines:
            self.place_mines(mines)
            self.add_values()
        print(self.__str__())

    def draw(self, screen):
        # Clear the screen and set the screen background

        y = MARGIN
        for row in range(self.height):
            x = MARGIN
            for column in range(self.width):
                self.board[row][column].draw(screen, x, y, self.helperProb) # draw tile
                x += WIDTH
            y += HEIGHT

    ''' Function to place the mines on the board
        Avoid exception and place mines
    '''
    def place_mines(self, mines, exception = None):
        '''
          Use random.sample() to place mines
        '''
        self.mines = mines
        if exception: # exception is a tuple containing the position of the tile to be avoided
            except_val = exception[0] * self.width + exception[1]
        if mines < self.height * self.width:
            sample = random.sample([i for i in range(0, self.height * self.width) if i != except_val], mines)
        else:
            print("Error: Sample larger than population!")
        for val in sample:
            i = val / self.width
            j = val % self.width
            self.board[i][j].value = 9

    def add_values(self):
        for i in range(0, self.width):
            for j in range(0, self.height):
                if self.board[i][j].value != 9:
                    neighbors = self.get_neighbors(i, j)
                    self.board[i][j].value = self.count_neighboring_mines(neighbors)
                    self.board[i][j].probability = round(float(self.mines) / self.tiles * 100.0, 1)

    def get_neighbors(self, row, col):
        # for a given cell return neighbors
        neighbors = [(row - 1, col - 1),(row - 1, col),(row - 1, col + 1),(row, col - 1),(row, col + 1),(row + 1, col - 1),(row + 1, col),(row + 1, col + 1)]
        true_neighbors = []
        for i in range(0,len(neighbors)):
            if 0 <= neighbors[i][0] < self.width and 0 <= neighbors[i][1] < self.height:
                true_neighbors.append((neighbors[i][0],neighbors[i][1]))
        return true_neighbors

    ''' The following function counts the number of mines in neighboring cells
    '''
    def count_neighboring_mines(self, neighbors):
        mines = 0
        for i in range(0, len(neighbors)):
            if self.board[neighbors[i][0]][neighbors[i][1]].value == 9:
                mines += 1
        return mines

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # change the board each time there is a click
                mouse_position = tuple((int(i) for i in event.pos))
                #cell = get_clicked_cell(board, mouse_position)

    '''Manages when a user clicks a tile
    '''
    def clicked(self, position, type):
        # if position off board don't do anything
        tile = self.pos_to_tile(position)
        if tile[0] >= 0 and tile[0] < self.width and tile[1] >= 0 and tile[1] < self.height:
            if type == 'left':
                if not self.board[tile[0]][tile[1]].flagged and not self.board[tile[0]][tile[1]].questioned:
                    self.board[tile[0]][tile[1]].revealed = True
                    if self.board[tile[0]][tile[1]].value == 9:
                        print("Game Over!")
                    elif self.board[tile[0]][tile[1]].value == 0:
                        self.automatic_reveal(tile[0], tile[1])
            elif type == 'right':
                if self.board[tile[0]][tile[1]].flagged:
                    self.board[tile[0]][tile[1]].flagged = False
                    self.board[tile[0]][tile[1]].questioned = True
                elif self.board[tile[0]][tile[1]].questioned:
                    self.board[tile[0]][tile[1]].questioned = False
                else:
                    self.board[tile[0]][tile[1]].flagged = True

    ''' Gets the tile that was clicked based on the mouse position on the screen
    '''
    def pos_to_tile(self, position):
        column = abs(position[0]) // (WIDTH)
        row = abs(position[1]) // (HEIGHT )
        return (row, column)

    def automatic_reveal(self, x, y):
        # We should be manipulating Tiles which would be easier
        # We should store in each Tile it's position on the board.
        neighbors = self.get_neighbors(x, y)
        for neighbor in neighbors:
            if self.board[neighbor[0]][neighbor[1]].value > 0 and self.board[neighbor[0]][neighbor[1]].revealed == False:
                self.board[neighbor[0]][neighbor[1]].revealed = True
            elif self.board[neighbor[0]][neighbor[1]].value == 0 and self.board[neighbor[0]][neighbor[1]].revealed == False:
                self.board[neighbor[0]][neighbor[1]].revealed = True
                self.automatic_reveal(neighbor[0], neighbor[1])

    def get_frontier(self):
        # gets all the Tiles that are at a boarder
        pass

    def compute_probability(self):
        # compute the probability of a mine in adjacent tiles
        '''
            Check if tile and neighboring Tiles follow a pattern:
            |     |     |     |
            |     |  T  |     |
            |     |     |     |
        '''
        for row in self.height:
            for col in self.width:
                tile = self.board[row][col]
                if self.board[row - 1][col].revealed  and self.board[row + 1][col].revealed and self.board[row - 1][col - 1].revealed and self.board[row + 1][col - 1]:
                    '''
                    |  O  |  O  |  F  |
                    |  O  |  T  |  F  |
                    |  O  |  O  |  F  |
                    '''
                    if tile.value == 2:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100
                    elif tile.value == 3:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100
                elif self.board[row - 1][col].revealed  and self.board[row + 1][col].revealed and self.board[row - 1][col + 1].revealed and self.board[row + 1][col + 1]:
                    '''
                    |  F  |  O  |  O  |
                    |  F  |  T  |  O  |
                    |  F  |  O  |  O  |
                    '''
                    if tile.value == 2:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100
                    elif tile.value == 3:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100
                elif self.board[row - 1][col].revealed  and self.board[row + 1][col].revealed and self.board[row - 1][col + 1].revealed and self.board[row + 1][col + 1]:
                    '''
                    |  O  |  O  |  O  |
                    |  O  |  T  |  O  |
                    |  F  |  F  |  F  |
                    '''
                    if tile.value == 2:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100
                    elif tile.value == 3:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100
                elif self.board[row - 1][col].revealed  and self.board[row + 1][col].revealed and self.board[row - 1][col + 1].revealed and self.board[row + 1][col + 1]:
                    '''
                    |  F  |  F  |  F  |
                    |  O  |  T  |  O  |
                    |  O  |  O  |  O  |
                    '''
                    if tile.value == 2:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100
                    elif tile.value == 3:
                        self.board[row - 1][col + 1].probability = 100
                        self.board[row][col + 1].probability = 100
                        self.board[row + 1][col + 1].probability = 100

    def helper1(self):
        # flag all obvious tiles
        pass

    def helper2(self):
        # reveal all obvious Tiles
        pass

    def helper3(self):
        # repeatedly do helper1 and helper2
        pass

    def helper4(self):
        # displays probability of tiles having a mine
        if not self.helperProb:
            self.helperProb = True
        else:
            self.helperProb = False

    def solver(self):
        # solves the minesweeper game
        pass

    def __str__(self):
        s = ""
        for row in range(self.height):
            for column in range(self.width):
                s += self.board[row][column].__str__()
            s += "\n"
        return s
