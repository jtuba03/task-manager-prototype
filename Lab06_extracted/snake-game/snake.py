#!/usr/bin/env python3
"""
Snake Game - Enhanced Version
Features: Power-ups (2x Score, Slow Down, Wrap-Around) and Lower Speed
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PINK = (255, 20, 147)
PURPLE = (148, 0, 211)
BLUE = (0, 100, 255)      # Slow Down
CYAN = (0, 255, 255)      # Wrap Around
GOLD = (255, 215, 0)      # 2x Score

NORMAL_FOOD_COLORS = [RED, ORANGE, PINK, PURPLE]

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Power-up Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        # Snake starts in the middle
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Moving right
        self.score = 0
        self.game_over = False
        
        # Power-up state (timers in frames)
        self.timers = {
            "DOUBLE_SCORE": 0,
            "SLOW_DOWN": 0,
            "WRAP_AROUND": 0
        }
        
        # Create multiple food items
        self.foods = []
        for _ in range(3):
            self.spawn_food()
    
    def spawn_food(self):
        """Spawn food with a chance of being a power-up"""
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if (x, y) not in self.snake and not any((x, y) == food[:2] for food in self.foods):
                # Determine food type
                rand = random.random()
                if rand < 0.1:
                    type, color = "DOUBLE_SCORE", GOLD
                elif rand < 0.2:
                    type, color = "SLOW_DOWN", BLUE
                elif rand < 0.3:
                    type, color = "WRAP_AROUND", CYAN
                else:
                    type, color = "NORMAL", random.choice(NORMAL_FOOD_COLORS)
                
                self.foods.append((x, y, color, type))
                break
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.direction != (0, 1):
            self.direction = (0, -1)
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.direction != (0, -1):
            self.direction = (0, 1)
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.direction != (-1, 0):
            self.direction = (1, 0)
    
    def update(self):
        if self.game_over:
            return
        
        # Update timers
        for power in self.timers:
            if self.timers[power] > 0:
                self.timers[power] -= 1
        
        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Handle Wall Collision or Wrap-Around
        if self.timers["WRAP_AROUND"] > 0:
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        else:
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                self.game_over = True
                return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check food collision
        food_eaten = False
        for i, food in enumerate(self.foods):
            if new_head[0] == food[0] and new_head[1] == food[1]:
                # Apply powers
                type = food[3]
                points = 20 if self.timers["DOUBLE_SCORE"] > 0 else 10
                self.score += points
                
                if type == "DOUBLE_SCORE":
                    self.timers["DOUBLE_SCORE"] = 150 # ~15 seconds at 10fps
                elif type == "SLOW_DOWN":
                    self.timers["SLOW_DOWN"] = 100
                elif type == "WRAP_AROUND":
                    self.timers["WRAP_AROUND"] = 200
                
                self.foods.pop(i)
                self.spawn_food()
                food_eaten = True
                break
        
        if not food_eaten:
            self.snake.pop()
    
    def draw_3d_food(self, x, y, color):
        pixel_x, pixel_y = x * GRID_SIZE, y * GRID_SIZE
        # Shadow
        shadow_color = tuple(max(0, c - 100) for c in color)
        pygame.draw.circle(self.screen, shadow_color, (pixel_x + 12, pixel_y + 12), 8)
        # Main
        pygame.draw.circle(self.screen, color, (pixel_x + 10, pixel_y + 10), 8)
        # Highlight
        pygame.draw.circle(self.screen, WHITE, (pixel_x + 7, pixel_y + 7), 3)

    def render(self):
        self.screen.fill(BLACK)
        
        # Draw Snake
        for i, segment in enumerate(self.snake):
            color = GREEN if i == 0 else DARK_GREEN
            # If wrap-around is active, make snake glow slightly
            if self.timers["WRAP_AROUND"] > 0:
                color = (100, 255, 100) if i == 0 else (50, 200, 50)
            
            pygame.draw.rect(self.screen, color, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1))
        
        # Draw Food
        for x, y, color, type in self.foods:
            self.draw_3d_food(x, y, color)
        
        # UI
        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (10, 10))
        
        # Active Power-ups display
        y_offset = 45
        for power, time in self.timers.items():
            if time > 0:
                p_text = f"{power.replace('_', ' ')}: {time // 10}s"
                color = GOLD if "DOUBLE" in power else (BLUE if "SLOW" in power else CYAN)
                text_surf = self.small_font.render(p_text, True, color)
                self.screen.blit(text_surf, (10, y_offset))
                y_offset += 20

        if self.game_over:
            msg = self.font.render("GAME OVER! Press R to restart", True, WHITE)
            self.screen.blit(msg, (WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2))
        
        pygame.display.flip()
    
    def run(self):
        print("Controls: WASD/Arrows to move, R to restart, ESC to quit")
        print("Special Foods: GOLD (2x Score), BLUE (Slow), CYAN (Wrap Walls)")
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: self.reset_game()
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            
            self.handle_input()
            self.update()
            self.render()
            
            # Base speed lowered to 10. Further slowed if SLOW_DOWN power is active.
            speed = 6 if self.timers["SLOW_DOWN"] > 0 else 10
            self.clock.tick(speed)

if __name__ == "__main__":
    SnakeGame().run()
