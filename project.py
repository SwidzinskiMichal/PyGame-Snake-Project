import pygame
import random

WINDOW = 800
TILE_SIZE = 50
screen = pygame.display.set_mode([WINDOW] * 2)
pygame.display.set_caption("Python")
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.x_position, self.y_position = TILE_SIZE, TILE_SIZE
        self.horizontal_direction = 1
        self.vertical_direction = 0
        self.head = pygame.Rect(self.x_position, self.y_position, TILE_SIZE, TILE_SIZE)
        self.body = [pygame.Rect(self.x_position - TILE_SIZE, self.y_position, TILE_SIZE, TILE_SIZE)]
        self.dead = False

    def update_position(self):
        self.body.append(self.head)
        for snake_tile_positon in range(len(self.body) - 1):
            self.body[snake_tile_positon].x = self.body[snake_tile_positon + 1].x
            self.body[snake_tile_positon].y = self.body[snake_tile_positon + 1].y
        self.head.x += self.horizontal_direction * TILE_SIZE
        self.head.y += self.vertical_direction * TILE_SIZE
        self.body.remove(self.head)


    def snake_movement(self, keys):
        if keys[pygame.K_w] and self.vertical_direction != 1:
            self.horizontal_direction = 0
            self.vertical_direction = -1       
        elif keys[pygame.K_s] and self.vertical_direction != -1:    
            self.horizontal_direction = 0
            self.vertical_direction = 1    
        elif keys[pygame.K_d] and self.horizontal_direction != -1:
            self.horizontal_direction = 1
            self.vertical_direction = 0   
        elif keys[pygame.K_a] and self.horizontal_direction != 1:
            self.horizontal_direction = -1
            self.vertical_direction = 0     

class Opponent:
    pass

def draw_grid():
    for  x_position in range(0, WINDOW, TILE_SIZE):
        for y_position in range(0, WINDOW, TILE_SIZE):
            rect = pygame.Rect(x_position, y_position, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, "dimgrey", rect, 1) 



# Main loop
           
draw_grid()
snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Thanks for playing!")
            exit()


    # Snake size and positon
    snake.snake_movement(pygame.key.get_pressed())
    snake.update_position()
    
    # Redraw the grid
    screen.fill("black")
    draw_grid()

    pygame.draw.rect(screen, "green", snake.head)
    for tile in snake.body:
        pygame.draw.rect(screen, "green", tile)

    

    pygame.display.update()
    clock.tick(10)