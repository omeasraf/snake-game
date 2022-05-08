import os, sys; sys.path.append(os.path.dirname(os.path.realpath('')))
import random
import pygame
# from .. import Direction, Point, BLOCK_SIZE, SPEED, GREEN3, RED1, BLACK, GREEN1, GREEN2, WHITE
from Direction import Direction, Point
from constants import BLOCK_SIZE, SPEED
from color_constants import GREEN3, RED1, BLACK, GREEN1, GREEN2, WHITE
import numpy as np
pygame.init() 

# Reset
# Reward
# Play(action) -> direction
# game_iteration
# is_collision

class SnakeGameAI:
    
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.is_hidden = False
        self.FONT = pygame.font.Font('../OleoScriptSwashCaps-Regular.ttf', 25)
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.reset()
        
        

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
    

    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        

        
    def play_step(self, action):
        self.frame_iteration += 1

        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        
        if not self.is_hidden:
        # move
            self._move(action) # update the head
            self.snake.insert(0, self.head)
        
        # check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = - 10
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED + (len(self.snake) / SPEED))
        # 6. return game over and score
        return reward, game_over, self.score


    
    # def is_collision(self, pt=None):
    #     if pt is None:
    #         pt = self.head
    #     # hits boundary
    #     if pt.x > self.width - BLOCK_SIZE or pt.x < 0 or pt.y > self.height - BLOCK_SIZE or pt.y < 0:
    #         return True
    #     # hits itself
    #     if pt in self.snake[1:]:
    #         return True
        
    #     return False
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt is self.head:
        # hits boundary
            self.is_hidden = True
            if pt.x > self.width - BLOCK_SIZE:
                self.head = Point(-BLOCK_SIZE, pt.y)
            elif pt.x < 0:
                self.direction = Direction.LEFT
                self.head = Point(self.width, pt.y)
            elif pt.y > self.height - BLOCK_SIZE:
                self.head = Point(pt.x, -BLOCK_SIZE)
            elif pt.y < 0:
                self.head = Point(pt.x, self.height)
            else:
                self.is_hidden = False
        else:
            self.is_hidden = False
            # return True
        
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
                        
    
            
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN3, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED1, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = self.FONT.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[next_idx]
        
        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
    