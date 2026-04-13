import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Physics
GRAVITY = 0.4
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_INTERVAL = 1500  # milliseconds
GROUND_HEIGHT = 50

class FlappyBirdGame:
    """Main class for the Flappy Bird game."""

    def __init__(self):
        """Initialize pygame and game state."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.large_font = pygame.font.SysFont("Arial", 48, bold=True)
        
        self.reset_game()

    def reset_game(self):
        """Reset the game state to its initial values."""
        self.bird_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, 30, 30)
        self.bird_vel = 0
        self.pipes = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()
        self.state = "START"  # States: START, PLAYING, PAUSED, GAME_OVER

    def spawn_pipe(self):
        """Create a new pipe with a random gap position."""
        gap_y = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100 - PIPE_GAP)
        # Top pipe
        top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, gap_y)
        # Bottom pipe
        bottom_pipe = pygame.Rect(SCREEN_WIDTH, gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - gap_y - PIPE_GAP - GROUND_HEIGHT)
        self.pipes.append({'top': top_pipe, 'bottom': bottom_pipe, 'passed': False})

    def handle_input(self):
        """Process keyboard and system events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.state == "START":
                        self.state = "PLAYING"
                        self.bird_vel = FLAP_STRENGTH
                    elif self.state == "PLAYING":
                        self.bird_vel = FLAP_STRENGTH
                    elif self.state == "GAME_OVER":
                        self.reset_game()
                
                if event.key == pygame.K_p:
                    if self.state == "PLAYING":
                        self.state = "PAUSED"
                    elif self.state == "PAUSED":
                        self.state = "PLAYING"
                
                if event.key == pygame.K_r:
                    self.reset_game()

    def update(self):
        """Update game physics and state."""
        if self.state != "PLAYING":
            return

        # Bird Physics
        self.bird_vel += GRAVITY
        self.bird_rect.y += int(self.bird_vel)

        # Pipe Spawning
        now = pygame.time.get_ticks()
        if now - self.last_pipe_time > PIPE_INTERVAL:
            self.spawn_pipe()
            self.last_pipe_time = now

        # Move Pipes and Check Score
        for pipe in self.pipes[:]:
            pipe['top'].x -= PIPE_SPEED
            pipe['bottom'].x -= PIPE_SPEED
            
            # Remove off-screen pipes
            if pipe['top'].right < 0:
                self.pipes.remove(pipe)
            
            # Increment score
            if not pipe['passed'] and pipe['top'].right < self.bird_rect.left:
                self.score += 1
                pipe['passed'] = True

        # Collision Detection
        self.check_collisions()

    def check_collisions(self):
        """Check for collisions with pipes, ground, and ceiling."""
        # Check pipes
        for pipe in self.pipes:
            if self.bird_rect.colliderect(pipe['top']) or self.bird_rect.colliderect(pipe['bottom']):
                self.state = "GAME_OVER"

        # Check floor and ceiling
        if self.bird_rect.top <= 0 or self.bird_rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.state = "GAME_OVER"

    def draw(self):
        """Render the game objects to the screen."""
        self.screen.fill(SKY_BLUE)

        # Draw Pipes
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, GREEN, pipe['top'])
            pygame.draw.rect(self.screen, GREEN, pipe['bottom'])
            # Pipe borders
            pygame.draw.rect(self.screen, BLACK, pipe['top'], 2)
            pygame.draw.rect(self.screen, BLACK, pipe['bottom'], 2)

        # Draw Ground
        pygame.draw.rect(self.screen, BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.draw.line(self.screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 5)

        # Draw Bird (Yellow circle with a small eye)
        pygame.draw.circle(self.screen, YELLOW, self.bird_rect.center, 15)
        pygame.draw.circle(self.screen, BLACK, self.bird_rect.center, 15, 2)
        # Eye
        eye_pos = (self.bird_rect.centerx + 8, self.bird_rect.centery - 5)
        pygame.draw.circle(self.screen, WHITE, eye_pos, 4)
        pygame.draw.circle(self.screen, BLACK, eye_pos, 2)

        # UI Overlay
        self.draw_ui()

        pygame.display.flip()

    def draw_ui(self):
        """Draw text overlays based on game state."""
        # Score
        score_surface = self.font.render(f"Score: {self.score}", True, BLACK)
        score_rect = score_surface.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(score_surface, score_rect)

        if self.state == "START":
            msg = self.font.render("Press SPACE to Start", True, BLACK)
            self.screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        
        elif self.state == "PAUSED":
            msg = self.large_font.render("PAUSED", True, BLACK)
            self.screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            sub_msg = self.font.render("Press P to Resume", True, BLACK)
            self.screen.blit(sub_msg, sub_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

        elif self.state == "GAME_OVER":
            msg = self.large_font.render("GAME OVER", True, BLACK)
            self.screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
            score_msg = self.font.render(f"Final Score: {self.score}", True, BLACK)
            self.screen.blit(score_msg, score_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))
            restart_msg = self.font.render("Press SPACE to Restart", True, BLACK)
            self.screen.blit(restart_msg, restart_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)))

    def run(self):
        """Start the main game loop."""
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
