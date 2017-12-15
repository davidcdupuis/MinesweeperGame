# http://programarcadegames.com/index.php?chapter=introduction_to_graphics&lang=en

# Python minesweeper game
import pygame
import numpy as np
import random
from settings import *
from classes import Tile
from classes import Board

# initialize the game engine
pygame.init()

size = (260, 260)
screen = pygame.display.set_mode(size)

# screen title
pygame.display.set_caption("My awesome minesweeper")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# ------------------ DRAWING -----------------------------------------
''' Function to draw the board on the screen
'''
def draw_board(board):
    # Clear the screen and set the screen background

    y = MARGIN
    for i in range(0, 10):
        x = MARGIN
        for j in range(0, 10):
            if board[i][j] == 9:
                pygame.draw.rect(screen, (255, 153, 153), [x, y, WIDTH, HEIGHT])
                pygame.draw.rect(screen, (255, 51, 51), [x, y, WIDTH, HEIGHT], 2)
                pygame.draw.rect(screen, (255, 0, 0), [x, y, WIDTH, HEIGHT], 1)
            elif board[i][j] == -1:
                pygame.draw.rect(screen, (0, 204, 0), [x, y, WIDTH, HEIGHT])
                pygame.draw.rect(screen, DARKGREY, [x, y, WIDTH, HEIGHT], 2)
                pygame.draw.rect(screen, DARKERGREY, [x, y, WIDTH, HEIGHT], 1)
            else:
                pygame.draw.rect(screen, GREY, [x, y, WIDTH, HEIGHT])
                pygame.draw.rect(screen, DARKGREY, [x, y, WIDTH, HEIGHT], 2)
                pygame.draw.rect(screen, DARKERGREY, [x, y, WIDTH, HEIGHT], 1)
            x += WIDTH
        y += HEIGHT


''' Function to draw the menu with the set of paramaters
'''
def draw_menu(params):
    pass


''' Function to count number of neighboring mines of a cell
'''
def add_values(board):
    ''' for each cell get all neighboring cells, count mines, assign number of mines to cell
    '''
    length = board.shape[0]
    width = board.shape[1]
    for i in range(0, length):
        for j in range(0, width):
            if board[i, j] != 9:
                neighbors = get_neighbors(i, j, board)
                board[i, j] = count_neighboring_mines(neighbors, board)

# ---------------------------------------------------------------------------

board = Board(10, 10, 10)

# -------- Main Program Loop -----------
# Loop until the user clicks the close button.
done = False
while not done:
    # --- Main event loop
    '''
    Detecting double clicks: at a guess, instead of processing each click immediately,
    apply a 50ms delay and see if you get another click event in that time. The user probably
    won't notice the 50ms delay.
    '''
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            # change the board each time there is a click
            mouse_position = tuple((int(i) for i in event.pos))
            board.clicked(mouse_position, 'left')
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            mouse_position = tuple((int(i) for i in event.pos))
            board.clicked(mouse_position, 'right')

    # --- Game logic should go here

    # --- Drawing code should go here
    screen.fill(WHITE)

    board.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
