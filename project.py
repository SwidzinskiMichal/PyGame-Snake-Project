import pygame
import random

WINDOW = 800
TILE_SIZE = 50
screen = pygame.display.set_mode([WINDOW] * 2)
pygame.display.set_caption("Python")
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.x, self.y = TILE_SIZE, WINDOW - 2 * TILE_SIZE
        self.horizontal_direction = 1
        self.vertical_direction = 0
        self.head = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        self.body = [pygame.Rect(self.x - TILE_SIZE, self.y, TILE_SIZE, TILE_SIZE)]
        self.dead = False

    def update_position(self):
        global opponents, wall
        for tile in self.body:
            if self.head.y == tile.y and self.head.x == tile.x:
                self.dead = True
        if self.head.y not in range(0, WINDOW) or self.head.x not in range(0, WINDOW):
            self.dead = True

            
        if self.dead:
            self.x, self.y = TILE_SIZE, WINDOW - 2 * TILE_SIZE
            self.horizontal_direction = 1
            self.vertical_direction = 0
            self.head = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
            self.body = [pygame.Rect(self.x - TILE_SIZE, self.y, TILE_SIZE, TILE_SIZE)]
            self.dead = False
            opponents = [Opponent() for opponent in range(3)]
            wall = [Wall(tile * 50) for tile in range(16)]
            entrance_index = random.randint(1, len(wall) - 2)
            wall.pop(entrance_index)
            wall.pop(entrance_index)
            wall.pop(entrance_index - 1)


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
    def __init__(self):
        self.x = int(random.randint(0, WINDOW) / TILE_SIZE) * TILE_SIZE
        self.y = int(random.randint(0, WINDOW) / TILE_SIZE) * TILE_SIZE
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def draw_opponent(self):
        pygame.draw.rect(screen, "red", self.rect)

class Wall:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def draw_wall(self):
        pygame.draw.rect(screen, "blue", self.rect)

def draw_grid():
    for  x_position in range(0, WINDOW, TILE_SIZE):
        for y_position in range(0, WINDOW, TILE_SIZE):
            rect = pygame.Rect(x_position, y_position, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, "dimgrey", rect, 1) 



# Main loop
total_frames_count = 0

draw_grid()
snake = Snake()
opponents = [Opponent() for opponent in range(3)]
wall = [Wall(tile * 50) for tile in range(16)]
entrance_index = random.randint(1, len(wall) - 2)
wall.pop(entrance_index)
wall.pop(entrance_index)
wall.pop(entrance_index - 1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Thanks for playing!")
            exit()

    if total_frames_count % 100 == 0:
        for opponent in opponents:
            opponent.y += 50
            opponent.rect = pygame.Rect(opponent.x, opponent.y, TILE_SIZE, TILE_SIZE)
            if opponent.y > 800:
                opponents.remove(opponent)
        for tile in wall:
            tile.y += 50
            tile.rect = pygame.Rect(tile.x, tile.y, TILE_SIZE, TILE_SIZE)
            if tile.y > 800:
                wall = [Wall(tile * 50) for tile in range(16)]
                entrance_index = random.randint(1, len(wall) - 2)
                wall.pop(entrance_index)
                wall.pop(entrance_index)
                wall.pop(entrance_index - 1)    
            
    # Snake size and positon
    snake.snake_movement(pygame.key.get_pressed())
    snake.update_position()
    
    # Redraw the grid
    screen.fill("black")
    draw_grid()

    pygame.draw.rect(screen, "green", snake.head)
    for tile in snake.body:
        pygame.draw.rect(screen, "green", tile)

    # Opponent position
    for opponent in opponents:
        opponent.draw_opponent()

    for tile in wall:
        tile.draw_wall()

    for opponent in opponents:
        if snake.head.x == opponent.x and snake.head.y == opponent.y:
            opponents.remove(opponent)
            if len(snake.body) < 6:
                snake.body.append(pygame.Rect(tile.x, tile.y, TILE_SIZE, TILE_SIZE))
        if wall[0].y == opponent.y:
            opponents.remove(opponent)

    if len(opponents) < 3:
        opponents.append(Opponent())


    total_frames_count += 4
    pygame.display.update()
    clock.tick(10)