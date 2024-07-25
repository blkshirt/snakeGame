import pygame
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

pygame.init()

# set the width and height of the screen [width, height]
size = (400, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Basic Snake Python Game")
clock = pygame.time.Clock()

# allow us to close the game
done = False

count = 0
grid = 16

class Snake:
  x = 160
  y = 160

  # snake velocity. moves one grid length every frame in either the x or y direction
  dx = grid
  dy = 0

  # keep track of all grids the snake body occupies
  cells = []

  # length of the snake. grows when eating an apple
  maxCells = 4

class Apple:
  x = 320
  y = 320

snake = Snake()
apple = Apple()

# game loop
while not done:
  # event loop
  for event in pygame.event.get():
    # listen to keyboard events to move the snake
    if event.type == pygame.KEYDOWN:
      # prevent snake from backtracking on itself by checking that it's
      # not already moving on the same axis (pressing left while moving
      # left won't do anything, and pressing right while moving left
      # shouldn't let you collide with your own body) 

      if event.key == pygame.K_LEFT and snake.dx == 0:
        snake.dx = -grid;
        snake.dy = 0;
      if event.key == pygame.K_UP and snake.dy == 0:
        snake.dy = -grid;
        snake.dx = 0;
      if event.key == pygame.K_RIGHT and snake.dx == 0:
        snake.dx = grid;
        snake.dy = 0;
      if event.key == pygame.K_DOWN and snake.dy == 0:
        snake.dy = grid;
        snake.dx = 0;

    # close when the X is clicked
    if event.type == pygame.QUIT:
      done = True

  # slow game updates to 15 per second instead of 60 (60/15 = 4)
  count += 1
  if count >= 4:
    # move snake by it's velocity
    snake.x += snake.dx;
    snake.y += snake.dy;

    # wrap snake position horizontally on edge of screen
    if snake.x < 0:
      snake.x = screen.get_width() - grid;
    elif snake.x >= screen.get_width():
      snake.x = 0;

    # wrap snake position vertically on edge of screen
    if snake.y < 0:
      snake.y = screen.get_height() - grid
    elif snake.y >= screen.get_height():
      snake.y = 0

    # keep track of where snake has been. front of the array is always the head
    snake.cells.append([snake.x, snake.y]);

    # remove cells as we move away from them
    if len(snake.cells) > snake.maxCells:
      snake.cells.pop(0)
    
    count = 0;

    screen.fill(BLACK)
  
    # draw apple
    pygame.draw.rect(screen, RED, pygame.Rect(apple.x, apple.y, grid - 1, grid - 1))

    # draw snake one cell at a time
    index = 0
    for cell in snake.cells:
      # drawing 1 px smaller than the grid creates a grid effect in the snake body so you can see how long it is
      pygame.draw.rect(screen, GREEN, pygame.Rect(cell[0], cell[1], grid - 1, grid - 1))

      # snake ate apple
      if cell[0] == apple.x and cell[1] == apple.y:
        snake.maxCells += 1

        # canvas is 400x400 which is 25x25 grids
        apple.x = random.randint(0, 24) * grid
        apple.y = random.randint(0, 24) * grid
      
      # check collision with all cells after this one (modified bubble sort)
      for i in range(index + 1, len(snake.cells)):
        # snake occupies same space as a body part. reset game
        if cell[0] == snake.cells[i][0] and cell[1] == snake.cells[i][1]:
          snake.x = 160
          snake.y = 160
          snake.cells = []
          snake.maxCells = 4
          snake.dx = grid
          snake.dy = 0

          apple.x = random.randint(0, 24) * grid
          apple.y = random.randint(0, 24) * grid
      
      index += 1

    # update the screen with what we've drawn.
    pygame.display.flip()

  # limit to 60 frames per second
  clock.tick(60)

# close the window and quit.
pygame.quit()