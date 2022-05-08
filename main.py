import pygame
pygame.init() 

from SnakeGame import SnakeGame

if __name__ == '__main__':
    game = SnakeGame()
    game.play()
pygame.quit()