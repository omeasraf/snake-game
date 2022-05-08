from tkinter import LEFT, RIGHT
from turtle import width
import pygame
import random
from enum import Enum
from collections import namedtuple;
import sys
import color_constants as cc


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point','x, y')
BLOCK_SIZE = 20
SPEED = 40



class SnakeGame:
    def __init__(self, display, width, height) -> None:

        self.width = width
        self.height = height

        # init display
        self.display = display
        pygame.display.set_caption("Snake Game")
    
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head, 
            Point(self.head.x - BLOCK_SIZE, self.head.y), 
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
            ]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()
        

    
    def play_step(self):
        # Collect user input

        # Move

        # Check if game over

        # Place new food

        # Update ui
        self._update_ui()
        self.clock.tick(SPEED)

        # return game over and score
        game_over = False
        return game_over, self.score
    
    def _update_ui(self):
        self.display.fill(cc.BLACK.color())

    def play_game(self):
        while True:
            game_over, score = game.play_step()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            

            # End game

            if game_over:
                break
        print(f"Final Score: {score}")




if __name__ == "__main__":
    pygame.init()
    width = 800
    height = 500
    display = pygame.display.set_mode((width, height))
    game = SnakeGame(display=display, width=width, height=height)
    game.play_game()

    pygame.quit()