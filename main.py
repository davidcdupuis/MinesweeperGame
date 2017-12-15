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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display(set_mode((260, 260)))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        #self.load_data()

    def load_data(self):
        pass

    def new(self):
        pass

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # self.all_sprites.update()
        pass

    def draw():
        self.screen.fill(WHITE)
        '''
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image)
        '''
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    pass
                elif event.button == RIGHT:
                    pass

    def draw_menu(self):
        pass


# ---------------------------------------------------------------------------

board = Board(10, 10)

# -------- Main Program Loop -----------
# Loop until the user clicks the close button.
done = False
first_click = True
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                mouse_position = tuple((int(i) for i in event.pos))
                if first_click:
                    first_click = False
                    board.place_mines(10, mouse_position)
                    board.add_values()
                    print("-----")
                    print(board)

                board.clicked(mouse_position, 'left')
            elif event.button == RIGHT:
                mouse_position = tuple((int(i) for i in event.pos))
                board.clicked(mouse_position, 'right')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # execute helper 1: place all obvious flags
                pass
            elif event.key == pygame.K_2:
                # execute helper 2: reveal all obvious tiles
                pass
            elif event.key == pygame.K_3:
                # executes helper 1 and 2 repeatedly until no more flags can be placed
                pass
            elif event.key == pygame.K_s:
                # execute solver to solve board
                pass



    # --- Game logic should go here

    # --- Drawing code should go here
    screen.fill(WHITE)

    board.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
