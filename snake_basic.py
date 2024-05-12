# https://www.youtube.com/watch?v=X2Wripo2Hxg

import pygame
import sys
import random

pygame.init()

class Snake:
    def __init__(self):
        # snake starts as 1 square in length
        self.length = 1
        # position is a list, so it can be appended as the snake eats,
        # initially it will start in the middle of the surface
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        # initially the direction of the snake is random
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = green

    def get_head_position(self):
        # the first item in the positions list is the position of the head
        return self.positions[0]

    def turn(self, point):
        # The snake turns by changing the sign (+/-) of the point coordinates by multiplying by -1
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current = self.get_head_position()
        x, y = self.direction
        # The new location coordinate is found by adding the current position and the direction coordinates.
        # GRID_SIZE and modulo are used so the snake will roll to the other side of the screen
        new = (((current[0] + (x * GRID_SIZE)) % WIDTH), (current[1] + (y * GRID_SIZE)) % HEIGHT)
        # The snake will reset if the new position is in the same location as one of the other positions
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        # This function resets the attributes to the original states.
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        # We use a for loop to draw each of the snake blocks iterating through the positions list
        # Rect class needs x,y for the location and a rectangle size (so we used the GRID_SIZE)
        for pos in self.positions:
            rect = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)

    def handle_keys(self):
        # The key presses in pygame are accepted using pygame.event.get() and the K_...
        for event in pygame.event.get():
            # lets the close window button close the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # KEYDOWN take the arrow keys and connects them to direction changes.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food:
    def __init__(self):
        self.position = (0,0)
        self.color = red
        self.randomize_position()

    def randomize_position(self):
        # For the random food location, we set the max range to the width-1 and height-1
        # so it won't be created off the surface.
        self.position = (random.randint(0,GRID_WIDTH-1)*GRID_SIZE, random.randint(0,GRID_HEIGHT-1)*GRID_SIZE)

    def draw(self, surface):
        # The draw function is copied from the snake class and edited for the food.
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)

def drawGrid(surface):
    # (0,0) in pygame is the top left
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            # Rect Class in pygame takes 2 arguments (x,y start coordinate), (width,height)
            rect = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, gray, rect)
            pygame.draw.rect(surface, dark_gray, rect, width=1)


# Game Variables
WIDTH = 400
HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
gray = (120, 120, 120)
dark_gray = (170, 170, 170)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
font = pygame.font.Font('freesansbold.ttf', 30)

# Directions
# Since the top left is (0,0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Main Game Loop
def main():

    # Clock class controls the frame rate in a pygame.
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    # Uses the pygame Surface class to create a playing surface on our game.
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    # Calling the drawGrid function in the beginning gives a grid before the game starts.
    drawGrid(surface)

    # Creates an instance of the Snake class and the Food class
    snake = Snake()
    food = Food()

    # Score starts at 0
    score = 0

    while True:
        # The Clock (fps) will control the speed of the snake.
        clock.tick(10)

        # Check for key presses.
        snake.handle_keys()

        # Calling the drawGrid function in the while loop draws the grid each time the loop cycles
        drawGrid(surface)

        # Call the move function and check to see if the snake ate the food.
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()

        # Redraw the snake
        snake.draw(surface)
        food.draw(surface)

        # Blit adds the surface to the screen
        screen.blit(surface, (0, 0))

        # Add the score to the screen at the location (5,10)
        text = font.render('Score {0}'.format(score), True, black)
        screen.blit(text, (5, 10))

        # The pygame.display.update function refreshes the display of the game each time the while loop cycles
        pygame.display.update()


# Calling the main function causes the game loop to run.
main()
