import pygame
import random
import sys
import time

# Constants for screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600  # Increased height for timer display
# CELL_SIZE = None
# MAZE_WIDTH = None
# MAZE_HEIGHT = None
TOP_MARGIN = 50
# TIME_LIMIT = None

# Color codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# List of levels with different cell sizes
LEVELS = [50, 40, 30, 20, 10]


# Function to generate a maze
def generateMaze(MAZE_WIDTH, MAZE_HEIGHT):
    # Initialize the maze with all walls
    maze = [[-1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

    # Function to create passages in the maze
    def createPassages(current_x, current_y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for direction_x, direction_y in directions:
            new_x, new_y = current_x + direction_x * 2, current_y + direction_y * 2
            if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] == -1:
                maze[current_y + direction_y][current_x + direction_x] = 0
                maze[new_y][new_x] = 0
                createPassages(new_x, new_y)

    # Start creating passages from the top-left corner
    maze[1][1] = 0
    createPassages(1, 1)
    # Set the exit point in the bottom-right corner
    maze[MAZE_HEIGHT - 2][MAZE_WIDTH - 2] = 1

    return maze


# Function to draw the maze
def drawMaze(screen, maze, cell_size):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == -1:
                pygame.draw.rect(screen, BLACK, (x * cell_size, y * cell_size + TOP_MARGIN, cell_size, cell_size))
            elif maze[y][x] == 1:
                pygame.draw.rect(screen, GREEN, (x * cell_size, y * cell_size + TOP_MARGIN, cell_size, cell_size))


# Class representing the player
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, maze):
        try:
            if maze[self.y + dy][self.x + dx] in [0, 1]:
                self.x += dx
                self.y += dy
                return True
        except Exception as e:
            return False

    def draw(self, screen, cell_size):
        pygame.draw.rect(screen, RED, (self.x * cell_size, self.y * cell_size + TOP_MARGIN, cell_size, cell_size))


# def checkWin(maze, player):
#     return maze[player.y][player.x] == 1

# Function to draw the restart and quit buttons
def drawButtons(screen, font):
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
    # next_level_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 190, 200, 50)
    pygame.draw.rect(screen, BLACK, restart_button)
    pygame.draw.rect(screen, BLACK, quit_button)
    restart_text = font.render("Restart", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2,
                               restart_button.y + (restart_button.height - restart_text.get_height()) // 2))
    screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                            quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

    return restart_button, quit_button


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + TOP_MARGIN))
    pygame.display.set_caption("2D Maze Game")
    font = pygame.font.Font(None, 36)

    # Start from the first level
    level = 0

    while True:
        # Set cell size and dimensions for the current level
        CELL_SIZE = LEVELS[level]
        MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE
        MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
        maze = generateMaze(MAZE_WIDTH, MAZE_HEIGHT)
        player = Player(1, 1)
        moves = 0
        TIME_LIMIT = 15 + (15 * level)
        start_time = time.time()
        elapsed_time = 0
        won = False
        running = True

        while running:
            elapsed_time = time.time() - start_time
            remaining_time = TIME_LIMIT - elapsed_time

            # Wait for button input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        is_done = player.move(0, -1, maze)
                        if is_done: moves += 1
                    elif event.key == pygame.K_DOWN:
                        is_done = player.move(0, 1, maze)
                        if is_done: moves += 1
                    elif event.key == pygame.K_LEFT:
                        is_done = player.move(-1, 0, maze)
                        if is_done: moves += 1
                    elif event.key == pygame.K_RIGHT:
                        is_done = player.move(1, 0, maze)
                        if is_done: moves += 1

            screen.fill(WHITE)
            drawMaze(screen, maze, CELL_SIZE)
            player.draw(screen, CELL_SIZE)

            # Display level, moves, and remaining time
            text = font.render(f"Level: {level+1} Moves: {moves} Time Left: {int(remaining_time)}s", True, BLACK)
            screen.blit(text, (10, 10))

            # Check if the player has reached the exit
            if maze[player.y][player.x] == 1:
                won = True
                running = False
            if remaining_time <= 0:
                running = False

            pygame.display.flip()

        # Display win/lose message and buttons
        if won:
            if level == (len(LEVELS)-1):
                win_text = font.render(f"Congrats! All Levels Cleared!", True, GREEN)
            else:
                win_text = font.render(f"Level {level+1} Cleared!", True, GREEN)
            moves_text = font.render("Moves Made: " + str(moves), True, GREEN)
            time_text = font.render("Time Taken: " + str(round(elapsed_time, 2)) + " seconds", True, GREEN)
            screen.fill(WHITE)
            screen.blit(win_text,
                        (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height()))
            screen.blit(moves_text, (SCREEN_WIDTH // 2 - moves_text.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(time_text,
                        (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 + time_text.get_height()))

            # If not the last level, display "Next Level" button
            if level != (len(LEVELS)-1):
                next_level_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
                pygame.draw.rect(screen, BLACK, next_level_button)
                next_level_text = font.render("Next Level", True, WHITE)
                screen.blit(next_level_text, (
                    next_level_button.x + (next_level_button.width - next_level_text.get_width()) // 2,
                    next_level_button.y + (next_level_button.height - next_level_text.get_height()) // 2))
            # Draw restart and quit buttons
            restart_button, quit_button = drawButtons(screen, font)
            pygame.display.flip()

            # Wait for button input
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        elif restart_button.collidepoint(event.pos):
                            level = 0
                            waiting_for_input = False
                        elif next_level_button.collidepoint(event.pos):
                            level += 1
                            waiting_for_input = False
        else:
            # If time runs out, display losing message
            time_up_text = font.render("Time's up", True, RED)
            lose_text = font.render("You Lost!", True, RED)
            screen.fill(WHITE)
            screen.blit(time_up_text,
                        (SCREEN_WIDTH // 2 - time_up_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_up_text.get_height()))
            screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, SCREEN_HEIGHT // 2))
            # Draw restart and quit buttons
            restart_button, quit_button = drawButtons(screen, font)
            pygame.display.flip()

            # Wait for button input
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        elif restart_button.collidepoint(event.pos):
                            level = 0
                            waiting_for_input = False


if __name__ == "__main__":
    main()
