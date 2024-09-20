import pygame
import random
 
 
# Initialize pygame
pygame.init()
 
 
# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Power-up: Increase basket size
CYAN = (0, 255, 255)  # Power-up: Slow down falling objects
PURPLE = (255, 0, 255)  # Power-up: Extra life
BASKET_WIDTH, BASKET_HEIGHT = 100, 20
OBJECT_WIDTH, OBJECT_HEIGHT = 30, 30
POWERUP_SIZE = 25
ORIGINAL_BASKET_WIDTH = BASKET_WIDTH
MAX_OBJECTS = 5  # Maximum number of falling objects on screen at once
INITIAL_LIVES = 3
LEVEL_CAP = 10  # Level 10 is the final level
MINIMUM_OBJECT_GAP = 100  # Minimum horizontal distance between objects
INITIAL_OBJECT_FREQUENCY = 100  # Initial spawn frequency
 
 
# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects - The Pycodes")
 
 
# Load fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
 
 
# Function to move the basket
def move_basket(basket, dx):
   basket.x += dx
   basket.x = max(0, min(WIDTH - basket.width, basket.x))
 
 
 
# Function to create a new falling object
def create_falling_object(speed_increase=0):
   rect = pygame.Rect(random.randint(0, WIDTH - OBJECT_WIDTH), 0, OBJECT_WIDTH, OBJECT_HEIGHT)
   speed = random.randint(2, 5 + speed_increase)
   return rect, speed
 
 
 
# Function to create a new power-up
def create_power_up():
   rect = pygame.Rect(random.randint(0, WIDTH - POWERUP_SIZE), 0, POWERUP_SIZE, POWERUP_SIZE)
   kind = random.choice(["increase_size", "slow_down", "extra_life"])
   return rect, kind
 
 
 
# Function to draw falling objects
def draw_falling_objects(falling_objects):
   for obj in falling_objects:
       pygame.draw.rect(screen, RED, obj[0])
 
 
# Function to draw power-ups
def draw_power_ups(power_ups):
   for pu in power_ups:
       if pu[1] == "increase_size":
           color = YELLOW
       elif pu[1] == "slow_down":
           color = CYAN
       elif pu[1] == "extra_life":
           color = PURPLE
       pygame.draw.rect(screen, color, pu[0])
 
 
# Function to reset basket size
def reset_basket_size(basket):
   basket.width = ORIGINAL_BASKET_WIDTH
 
 
 
# Button drawing function
def draw_button(text, x, y, width, height, color):
   rect = pygame.Rect(x, y, width, height)
   pygame.draw.rect(screen, color, rect)
   text_surf = font.render(text, True, WHITE)
   text_rect = text_surf.get_rect(center=rect.center)
   screen.blit(text_surf, text_rect)
   return rect
 
 
 
# Main game function
def game():
   clock = pygame.time.Clock()
   basket = pygame.Rect(WIDTH // 2, HEIGHT - BASKET_HEIGHT - 10, BASKET_WIDTH, BASKET_HEIGHT)
   falling_objects = []
   power_ups = []
   score = 0
   level = 1
   lives = INITIAL_LIVES
   speed_increase = 0
   power_up_timer = 0
   slow_down_timer = 0
   game_active = False
   game_over = False
   game_won = False  # Track whether the game was won
   object_frequency = INITIAL_OBJECT_FREQUENCY  # Use the initial frequency
   object_spawn_counter = 0
 
 
   # Buttons
   start_button_rect = draw_button("Start", WIDTH // 2 - 75, HEIGHT // 2 - 40, 150, 80, GREEN)
   restart_button_rect = draw_button("Restart", WIDTH // 2 - 75, HEIGHT // 2 - 40, 150, 80, GREEN)
 
 
   running = True
   while running:
       clock.tick(FPS)
 
 
       # Handle events
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           if event.type == pygame.MOUSEBUTTONDOWN:
               if not game_active and not game_over and not game_won and start_button_rect.collidepoint(event.pos):
                   game_active = True
               if (game_over or game_won) and restart_button_rect.collidepoint(event.pos):
                   score, level, speed_increase, lives = 0, 1, 0, INITIAL_LIVES
                   reset_basket_size(basket)
                   falling_objects.clear()
                   power_ups.clear()
                   object_frequency = INITIAL_OBJECT_FREQUENCY  # Reset spawn frequency
                   object_spawn_counter = 0  # Reset spawn counter
                   game_active = True
                   game_over = False
                   game_won = False
 
 
       # Get keys
       keys = pygame.key.get_pressed()
       if game_active:
           if keys[pygame.K_LEFT]:
               move_basket(basket, -10)
           if keys[pygame.K_RIGHT]:
               move_basket(basket, 10)
 
 
       # Spawn new falling objects based on level and frequency
       if game_active:
           object_spawn_counter += 1
           if object_spawn_counter >= object_frequency and len(falling_objects) < MAX_OBJECTS:
               # Ensure the new object does not spawn too close to another object
               new_object = create_falling_object(speed_increase)
               if all(abs(new_object[0].x - obj[0].x) > MINIMUM_OBJECT_GAP for obj in falling_objects):
                   falling_objects.append(new_object)
                   object_spawn_counter = 0  # Reset the counter
 
 
           # Spawn power-ups occasionally
           if random.randint(0, 400) == 0:
               power_ups.append(create_power_up())
 
 
       # Update falling objects
       if game_active:
           # Iterate in reverse to safely remove items
           for i in range(len(falling_objects) - 1, -1, -1):
               rect, speed = falling_objects[i]
               rect.y += speed  # Move object downward
               if rect.y > HEIGHT:
                   falling_objects.pop(i)  # Remove object if it falls off the screen
                   lives -= 1
                   if lives <= 0:
                       game_active = False
                       game_over = True
               elif rect.colliderect(basket):
                   falling_objects.pop(i)
                   score += 1
                   if score % 10 == 0 and level < LEVEL_CAP:  # Increase level every 10 points
                       level += 1
                       speed_increase += 1
                       object_frequency = max(INITIAL_OBJECT_FREQUENCY - (level * 10), 20)  # Increase difficulty
 
 
       # If player reaches level 10 and completes it
       if level == LEVEL_CAP and score % 10 == 0 and score > 0:
           game_active = False
           game_won = True
 
 
       # Update power-ups
       if game_active:
           # Iterate in reverse to safely remove items
           for i in range(len(power_ups) - 1, -1, -1):
               rect, kind = power_ups[i]
               rect.y += 5  # Move power-up downward
               if rect.y > HEIGHT:
                   power_ups.pop(i)
               elif rect.colliderect(basket):
                   power_ups.pop(i)
                   if kind == "increase_size":
                       basket.width = int(ORIGINAL_BASKET_WIDTH * 1.5)
                       power_up_timer = 300  # Basket stays larger for a short period
                   elif kind == "slow_down":
                       slow_down_timer = 300  # Slows down objects for a short period
                   elif kind == "extra_life":
                       lives += 1
 
 
       # Handle power-up effects timing
       if power_up_timer > 0:
           power_up_timer -= 1
       else:
           reset_basket_size(basket)
 
 
       if slow_down_timer > 0:
           slow_down_timer -= 1
           # Update the speed of all objects
           for i in range(len(falling_objects)):
               rect, speed = falling_objects[i]
               falling_objects[i] = (rect, max(1, speed - 1))
       else:
           for i in range(len(falling_objects)):
               rect, _ = falling_objects[i]
               falling_objects[i] = (rect, random.randint(2, 5 + speed_increase))
 
 
       # Drawing
       if game_active:
           screen.fill(WHITE)
           # Draw basket and falling objects
           pygame.draw.rect(screen, BLUE, basket)
           draw_falling_objects(falling_objects)
           draw_power_ups(power_ups)
 
 
           # Display score, level, and lives
           score_text = font.render(f"Score: {score}", True, BLACK)
           level_text = font.render(f"Level: {level}", True, BLACK)
           lives_text = font.render(f"Lives: {lives}", True, BLACK)
           screen.blit(score_text, (10, 10))
           screen.blit(level_text, (10, 50))
           screen.blit(lives_text, (10, 90))
 
 
       elif not game_active and not game_over and not game_won:
           # Display start screen
           screen.fill(BLACK)
           title_text = large_font.render("Catch the Objects!", True, GREEN)
           screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 120))
           start_button_rect = draw_button("Start", WIDTH // 2 - 75, HEIGHT // 2 - 40, 150, 80, GREEN)
 
 
       elif game_over:
           # Display game over screen
           screen.fill(BLACK)
           game_over_text = large_font.render("Game Over", True, RED)
           screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
 
 
           final_score_text = font.render(f"Final Score: {score}", True, WHITE)
           screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 50))
 
 
           restart_button_rect = draw_button("Restart", WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 80, GREEN)
 
 
       elif game_won:
           # Display congratulations screen
           screen.fill(BLACK)
           congrats_text = large_font.render("Congratulations! You Won!", True, GREEN)
           screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - 150))
 
 
           final_score_text = font.render(f"Final Score: {score}", True, WHITE)
           screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 50))
 
 
           restart_button_rect = draw_button("Restart", WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 80, GREEN)
 
 
       pygame.display.flip()
 
 
   pygame.quit()
 
 
# Run the game
if __name__ == "__main__":
   game()
