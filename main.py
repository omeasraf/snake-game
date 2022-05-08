import pygame
from SnakeGame import SnakeGame

pygame.init() 

if __name__ == '__main__':
    game = SnakeGame()
    game.play()
pygame.quit()