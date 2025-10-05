import pygame
import random
import time

# Initialize all imported pygame modules
pygame.init()

# Set screen dimensions (width x height in pixels)
width, height = 800, 700

# Define colors using RGB values
white = (255, 255, 255)
# green = (0, 255, 0)   # (Optional color if you want to use later)
red = (255, 0, 0)
black = (0, 0, 0)

# Create and initialize the game screen (window)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")  # Set window title

# Snake initial position (head of the snake)
snake_pos = [100, 50]

# Snake body segments (list of positions: head + body parts)
snake_body = [[100, 50], [90, 50], [80, 50]]

# Generate random food position (aligned to grid of 10x10)
food_pos = [random.randrange(1, (width // 10)) * 10,
            random.randrange(1, (height // 10)) * 10]
food_spawn = True  # Boolean flag to control food spawning

# Snake starting direction
direction = 'RIGHT'
# Variable to store next direction (prevents snake reversing instantly)
change_to = direction

# Game score counter
score = 0


# Function to handle game over screen and exit
def game_over():
    font = pygame.font.SysFont('Arial', 50)  # Create font object
    text = font.render('Game Over', True, red)  # Render "Game Over" text
    # Draw text in the center of the screen
    screen.blit(text, (width // 2 - 100, height // 2 - 25))
    pygame.display.update()  # Update the display to show text
    time.sleep(2)  # Pause for 2 seconds
    pygame.quit()  # Uninitialize pygame
    quit()  # Exit the program


# ---------------- MAIN GAME LOOP ----------------
while True:
    # Handle user input (events like key presses)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # If a key is pressed
            # Change direction only if it's not the opposite of current direction
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Update snake's direction based on input
    if change_to == 'UP':
        direction = 'UP'
    elif change_to == 'DOWN':
        direction = 'DOWN'
    elif change_to == 'LEFT':
        direction = 'LEFT'
    elif change_to == 'RIGHT':
        direction = 'RIGHT'

    # Update snake's head position (movement)
    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10

    # Insert new head position at the beginning of the body list
    snake_body.insert(0, list(snake_pos))

    # Check if snake has eaten food
    if snake_pos == food_pos:
        score += 1  # Increase score
        food_spawn = False  # Disable spawning until next cycle
    else:
        # Remove last block of snake body (unless food eaten)
        snake_body.pop()

    # If food was eaten, spawn a new one at a random position
    if not food_spawn:
        food_pos = [random.randrange(1, (width // 10)) * 10,
                    random.randrange(1, (height // 10)) * 10]
    food_spawn = True

    # ---------------- GAME OVER CONDITIONS ----------------
    # Snake hits left or right boundary
    if snake_pos[0] < 0 or snake_pos[0] > width - 10:
        game_over()
    # Snake hits top or bottom boundary
    if snake_pos[1] < 0 or snake_pos[1] > height - 10:
        game_over()
    # Snake collides with itself
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # ---------------- RENDERING SECTION ----------------
    screen.fill(black)  # Fill background with black

    # Draw the snake body (white squares)
    for pos in snake_body:
        pygame.draw.rect(screen, white, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the food (white square)
    pygame.draw.rect(screen, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Refresh game screen
    pygame.display.update()

    # Control the speed of the game (15 frames per second)
    pygame.time.Clock().tick(15)