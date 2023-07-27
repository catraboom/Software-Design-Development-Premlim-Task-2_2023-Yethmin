import pygame
import sys

# Game constants
GRID_SIZE = 11  # Size of the grid (11x11)
CELL_SIZE = 50  # Size of each cell (50x50 pixels)
PADDING_TOP = 50  # Padding on top of the grid (50 pixels)
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, (GRID_SIZE * CELL_SIZE) + PADDING_TOP)
PLAYER_COLOR = (66, 73, 255)  # Blue Player colour
PLAYER_2_COLOR = (255, 66, 66)  # Red Player 2 colour
FONT_SIZE = 20  # Font size (20 pixels)
FONT_COLOR = (0, 0, 0)  # Black font colour
FONT_COLOR_2 = (255, 255, 255)  # White font colour
CUSTOM_FONT_FILE = 'Main Game\Fonts\Minecraftia.ttf'  # Custom font file
PLAYER_SOUND_FILE = 'Main Game\Sound Effects\ding-idea-40142_ljQkHJgG.wav'  # Custom player move sound file
PLAYER_SOUND_FILE_2 = 'Main Game\Sound Effects\pop-1-35897.mp3'  # Custom player 2 move sound file
WINNER_SOUND_FILE = 'Main Game\Sound Effects\mixkit-winning-chimes-2015.wav'  # Custom winner sound file

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)  # Create the window
clock = pygame.time.Clock()  # Create the clock
custom_font = pygame.font.Font(CUSTOM_FONT_FILE, FONT_SIZE)  # Create the font

# Create the grid
grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]

# Load and resize the custom image
background_image = pygame.image.load(
    'Main Game\Backgrounds\DALL·E 2023-07-15 21.20.00 - digital art depicting a hexagon background with various shades of green.png'
)  # Custom background image
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)  # Resize the image to fit the window

# Create a copy of the image to modify its transparency
background_copy = background_image.copy()

# Set the transparency level (0-255) on the copied image surface
alpha_value = 200  # Change this value to adjust transparency
background_copy.set_alpha(alpha_value)  # Set the transparency level

# Load the sounds
player_sound = pygame.mixer.Sound(PLAYER_SOUND_FILE)  # Custom player move sound
player_2_sound = pygame.mixer.Sound(PLAYER_SOUND_FILE_2)  # Custom player 2 move sound
winner_sound = pygame.mixer.Sound(WINNER_SOUND_FILE)  # Custom winner sound

# Flag to track if the winner sound has been played
winner_sound_played = False

def draw_grid():
    window.fill((255, 255, 255))  # Fill the window with white
    window.blit(background_copy, (0, 0))  # Draw the background image

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(
                col * CELL_SIZE, (row * CELL_SIZE) + PADDING_TOP, CELL_SIZE, CELL_SIZE
            )  # Creates the grid's rectangles
            pygame.draw.rect(window, (0, 0, 0), rect, 1)  # Draw grid lines

            if grid[row][col] == 'player':
                pygame.draw.rect(window, PLAYER_COLOR, rect)  # Draw player's square
            elif grid[row][col] == 'player_2':
                pygame.draw.rect(window, PLAYER_2_COLOR, rect)  # Draw Player 2's square

    pygame.display.update()

def is_valid_move(row, col):
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] is None  # Check if the move is valid

def check_winner():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] is not None:
                # Check horizontal line
                if col + 3 < GRID_SIZE and all(grid[row][c] == grid[row][col] for c in range(col, col + 4)):
                    return grid[row][col]

                # Check vertical line
                if row + 3 < GRID_SIZE and all(grid[r][col] == grid[row][col] for r in range(row, row + 4)):
                    return grid[row][col]

                # Check diagonal lines
                if row + 3 < GRID_SIZE and col + 3 < GRID_SIZE:
                    if all(grid[row + i][col + i] == grid[row][col] for i in range(4)):
                        return grid[row][col]
                    if all(grid[row + i][col - i] == grid[row][col] for i in range(4)):
                        return grid[row][col]

    return None

def display_winner(winner):
    global winner_sound_played

    if winner == 'player':
        text = custom_font.render("Player 1 wins!", True, FONT_COLOR)
    elif winner == 'player_2':
        text = custom_font.render("Player 2 wins!", True, FONT_COLOR)
    else:
        text = custom_font.render("It's a tie!", True, FONT_COLOR)

    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, PADDING_TOP // 2))
    window.blit(text, text_rect)
    if not winner_sound_played:  # Check if the winner sound has not been played
        winner_sound.play()  # Play the winner sound
        winner_sound_played = True  # Set the flag to True

def reset_game():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = None

# Game loop
restart_game = False
current_player = 'player'

while True: # Main game loop
    if restart_game:
        reset_game()
        restart_game = False
        current_player = 'player'
        winner_sound_played = False  # Reset the winner sound played flag
    game_over = False
    winner = None

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # Player's move
                mouse_pos = pygame.mouse.get_pos()
                row = (mouse_pos[1] - PADDING_TOP) // CELL_SIZE
                col = mouse_pos[0] // CELL_SIZE

                if is_valid_move(row, col):
                    grid[row][col] = current_player
                    winner = check_winner()
                    if winner is not None:
                        game_over = True
                    else:
                        # Switch to the other player after a move
                        current_player = 'player_2' if current_player == 'player' else 'player'
                        if current_player == 'player_2':
                            player_2_sound.play()  # Play the player 2 move sound
                        else:
                            player_sound.play()  # Play the player move sound

        draw_grid()
        clock.tick(60)  # Limit the frame rate to 60 FPS

    # Game over loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game = True

        if restart_game:
            break

        display_winner(winner)  # Display the winner
        text = custom_font.render("Press 'R' to play again", True, FONT_COLOR_2)  # Display the restart message
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - (PADDING_TOP // 2)))  # Center the text
        window.blit(text, text_rect)  # Display the text
        pygame.display.update()  # Update the display
