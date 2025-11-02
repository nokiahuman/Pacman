import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game map (1 = wall, 0 = path, 2 = pellet, 3 = power pellet)
GAME_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,2,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,2,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,2,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1,1,1,1,0,0,1,1,1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1],
    [2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,1,0,0,0,0,0,0,0,0,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2],
    [1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,0,0,0,0,0,0,0,0,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,1,1,2,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,2,0,0,2,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,2,2,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,2,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROWS = len(GAME_MAP)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = [0, 0]
        self.next_direction = [0, 0]
        self.speed = 2
        self.radius = CELL_SIZE // 2 - 2
        self.mouth_angle = 0
        self.mouth_open = True
        
    def update(self):
        # Try to change direction
        if self.can_move(self.next_direction):
            self.direction = self.next_direction.copy()
        
        # Move if possible
        if self.can_move(self.direction):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
            
        # Wrap around screen edges
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
            
        # Animate mouth
        self.mouth_angle += 5
        if self.mouth_angle > 20:
            self.mouth_angle = 0
            self.mouth_open = not self.mouth_open
    
    def can_move(self, direction):
        new_x = self.x + direction[0] * self.speed
        new_y = self.y + direction[1] * self.speed
        
        # Check collision with walls
        col = int(new_x // CELL_SIZE)
        row = int(new_y // CELL_SIZE)
        
        if 0 <= row < ROWS and 0 <= col < COLS:
            if GAME_MAP[row][col] == 1:
                return False
        return True
    
    def get_grid_pos(self):
        return int(self.y // CELL_SIZE), int(self.x // CELL_SIZE)
    
    def draw(self, screen):
        if self.mouth_open:
            start_angle = math.radians(self.mouth_angle)
            end_angle = math.radians(360 - self.mouth_angle)
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
            pygame.draw.polygon(screen, BLACK, [
                (int(self.x), int(self.y)),
                (int(self.x + self.radius * math.cos(start_angle)), int(self.y - self.radius * math.sin(start_angle))),
                (int(self.x + self.radius * math.cos(end_angle)), int(self.y - self.radius * math.sin(end_angle)))
            ])
        else:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

class Ghost:
    def __init__(self, x, y, color):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.speed = 1.5  # Set speed before find_initial_direction() needs it
        self.radius = CELL_SIZE // 2 - 2
        self.color = color
        self.scared = False
        self.scared_timer = 0
        # Initialize with a random valid direction
        self.direction = self.find_initial_direction()
        
    def find_initial_direction(self):
        """Find a valid initial direction for the ghost"""
        choices = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        random.shuffle(choices)
        for choice in choices:
            if self.can_move(choice):
                return choice
        return [1, 0]  # Default to right if no valid direction found
        
    def is_at_intersection(self):
        """Check if ghost is approximately aligned to grid (at intersection)"""
        grid_x = round(self.x / CELL_SIZE) * CELL_SIZE
        grid_y = round(self.y / CELL_SIZE) * CELL_SIZE
        return abs(self.x - grid_x) < self.speed and abs(self.y - grid_y) < self.speed
    
    def update(self, pacman):
        if self.scared:
            self.scared_timer -= 1
            if self.scared_timer <= 0:
                self.scared = False
        
        # Check if ghost can continue in current direction
        if not self.can_move(self.direction):
            # Must change direction immediately
            if self.scared:
                self.move_random()
            else:
                self.move_towards_pacman(pacman)
        elif self.is_at_intersection():
            # At intersection, consider changing direction
            if self.scared:
                # Occasionally change direction when scared (30% chance)
                if random.random() < 0.3:
                    self.move_random()
            else:
                # Always recalculate best direction towards pacman at intersections
                self.move_towards_pacman(pacman)
        
        # Move ghost
        if self.can_move(self.direction):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
        else:
            # Emergency: if still can't move, try to find any valid direction
            choices = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            random.shuffle(choices)
            for choice in choices:
                if self.can_move(choice):
                    self.direction = choice
                    self.x += self.direction[0] * self.speed
                    self.y += self.direction[1] * self.speed
                    break
        
        # Wrap around
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
    
    def move_random(self):
        choices = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        # Don't reverse direction unless necessary
        reverse_dir = [-self.direction[0], -self.direction[1]]
        valid_choices = [c for c in choices if c != reverse_dir and self.can_move(c)]
        
        if not valid_choices:
            # If no forward/left/right options, allow reverse
            valid_choices = [c for c in choices if self.can_move(c)]
        
        if valid_choices:
            random.shuffle(valid_choices)
            self.direction = valid_choices[0]
        # If no valid direction found, keep current direction (will be handled in update)
    
    def move_towards_pacman(self, pacman):
        # Simple pathfinding: try to move towards pacman
        choices = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        
        # Don't reverse direction unless it's the best option
        reverse_dir = [-self.direction[0], -self.direction[1]]
        valid_choices = [c for c in choices if c != reverse_dir and self.can_move(c)]
        
        # If no valid forward directions, allow reverse
        if not valid_choices:
            valid_choices = [c for c in choices if self.can_move(c)]
        
        if not valid_choices:
            # No valid moves, keep current direction
            return
        
        # Score each valid direction
        best_dir = self.direction
        best_score = float('inf')
        
        for choice in valid_choices:
            new_x = self.x + choice[0] * self.speed * 5  # Look ahead further
            new_y = self.y + choice[1] * self.speed * 5
            dist = math.sqrt((new_x - pacman.x)**2 + (new_y - pacman.y)**2)
            if dist < best_score:
                best_score = dist
                best_dir = choice
        
        self.direction = best_dir
    
    def can_move(self, direction):
        if direction == [0, 0]:
            return False
            
        new_x = self.x + direction[0] * self.speed
        new_y = self.y + direction[1] * self.speed
        
        # Check multiple points along the path for better collision detection
        for offset in [0, 0.5, 1.0]:
            check_x = self.x + direction[0] * self.speed * offset
            check_y = self.y + direction[1] * self.speed * offset
            
            col = int(check_x // CELL_SIZE)
            row = int(check_y // CELL_SIZE)
            
            if 0 <= row < ROWS and 0 <= col < COLS:
                if GAME_MAP[row][col] == 1:
                    return False
            # Also check bounds
            if row < 0 or row >= ROWS or col < 0 or col >= COLS:
                # Allow wrapping at edges (for tunnel areas)
                pass
                
        return True
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = self.find_initial_direction()
        self.scared = False
        self.scared_timer = 0
    
    def draw(self, screen):
        color = BLUE if self.scared else self.color
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        # Draw eyes
        eye_offset = 3
        pygame.draw.circle(screen, WHITE, (int(self.x - eye_offset), int(self.y - 2)), 2)
        pygame.draw.circle(screen, WHITE, (int(self.x + eye_offset), int(self.y - 2)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x - eye_offset), int(self.y - 2)), 1)
        pygame.draw.circle(screen, BLACK, (int(self.x + eye_offset), int(self.y - 2)), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Initialize game objects
        self.pacman = Pacman(CELL_SIZE * 10, CELL_SIZE * 15)
        self.ghosts = [
            Ghost(CELL_SIZE * 10, CELL_SIZE * 10, RED),
            Ghost(CELL_SIZE * 19, CELL_SIZE * 10, PINK),
            Ghost(CELL_SIZE * 10, CELL_SIZE * 9, CYAN),
            Ghost(CELL_SIZE * 19, CELL_SIZE * 9, ORANGE),
        ]
        
        self.score = 0
        self.lives = 3
        self.running = True
        self.game_over = False
        self.won = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = [0, 1]
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = [1, 0]
                elif event.key == pygame.K_r and (self.game_over or self.won):
                    self.__init__()
    
    def check_collisions(self):
        # Check pellet collection
        row, col = self.pacman.get_grid_pos()
        if 0 <= row < ROWS and 0 <= col < COLS:
            if GAME_MAP[row][col] == 2:
                GAME_MAP[row][col] = 0
                self.score += 10
            elif GAME_MAP[row][col] == 3:
                GAME_MAP[row][col] = 0
                self.score += 50
                # Make all ghosts scared
                for ghost in self.ghosts:
                    ghost.scared = True
                    ghost.scared_timer = 300
        
        # Check ghost collisions
        for ghost in self.ghosts:
            dist = math.sqrt((self.pacman.x - ghost.x)**2 + (self.pacman.y - ghost.y)**2)
            if dist < self.pacman.radius + ghost.radius:
                if ghost.scared:
                    ghost.reset()
                    self.score += 200
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.pacman.x = CELL_SIZE * 10
                        self.pacman.y = CELL_SIZE * 15
                        self.pacman.direction = [0, 0]
                        self.pacman.next_direction = [0, 0]
        
        # Check win condition
        pellets_left = sum(row.count(2) + row.count(3) for row in GAME_MAP)
        if pellets_left == 0:
            self.won = True
    
    def draw_map(self):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                if GAME_MAP[row][col] == 1:
                    pygame.draw.rect(self.screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                elif GAME_MAP[row][col] == 2:
                    pygame.draw.circle(self.screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 2)
                elif GAME_MAP[row][col] == 3:
                    pygame.draw.circle(self.screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 6)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if not self.game_over and not self.won:
            self.draw_map()
            self.pacman.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            
            # Draw score and lives
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
        else:
            if self.won:
                text = self.font.render("YOU WON! Press R to restart", True, WHITE)
            else:
                text = self.font.render("GAME OVER! Press R to restart", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, text_rect)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            self.screen.blit(score_text, score_rect)
        
        pygame.display.flip()
    
    def update(self):
        if not self.game_over and not self.won:
            self.pacman.update()
            for ghost in self.ghosts:
                ghost.update(self.pacman)
            self.check_collisions()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

