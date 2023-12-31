import pygame
import sys

# Game constants
GRID_SIZE = 11 # Size of the grid (11x11)
CELL_SIZE = 50 # Size of each cell (50x50 pixels)
PADDING_TOP = 50 # Padding on top of the grid (50 pixels)
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, (GRID_SIZE * CELL_SIZE) + PADDING_TOP)
PLAYER_COLOUR = (66, 73, 255)  # Blue Player colour
AI_COLOUR = (255, 66, 66)  # Red AI colour
FONT_SIZE = 20 # Font size (20 pixels)
FONT_COLOUR = (0, 0, 0)  # Black font colour
FONT_COLOUR_2 = (255, 255, 255)  # White font colour
CUSTOM_FONT_FILE = 'Main Game\Fonts\Minecraftia.ttf' # Custom font file
PLAYER_SOUND_FILE = 'Main Game\Sound Effects\ding-idea-40142_ljQkHJgG.wav'  # Custom player move sound file
AI_SOUND_FILE = 'Main Game\Sound Effects\mixkit-arcade-robot-sound-1415_OiPFfAGb.wav'  # Custom AI sound file
WINNER_SOUND_FILE = 'Main Game\Sound Effects\mixkit-winning-chimes-2015.wav'  # Custom winner sound file
WIN_SCORE = 1000
LOSS_SCORE = -1000
INFINITY = float('inf')

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE) # Create the window
clock = pygame.time.Clock() # Create the clock
custom_font = pygame.font.Font(CUSTOM_FONT_FILE, FONT_SIZE) # Create the font

# Create the grid
grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]

# Load and resize the custom image
background_image = pygame.image.load('Main Game\Backgrounds\DALL·E 2023-07-15 21.20.00 - digital art depicting a hexagon background with various shades of green.png') # Custom background image
background_image = pygame.transform.scale(background_image, WINDOW_SIZE) # Resize the image to fit the window

# Create a copy of the image to modify its transparency
background_copy = background_image.copy()

# Set the transparency level (0-255) on the copied image surface
alpha_value = 200  # Change this value to adjust transparency
background_copy.set_alpha(alpha_value) # Set the transparency level

# Load the sounds
player_sound = pygame.mixer.Sound(PLAYER_SOUND_FILE) # Custom player move sound
ai_sound = pygame.mixer.Sound(AI_SOUND_FILE) # Custom AI sound
winner_sound = pygame.mixer.Sound(WINNER_SOUND_FILE) # Custom winner sound

# Flag to track if the winner sound has been played
winner_sound_played = False

ai_last_move_time = 0  # Time when the AI last moved

def draw_grid():
    window.fill((255, 255, 255))  # Fill the window with white
    window.blit(background_copy, (0, 0))  # Draw the background image

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, (row * CELL_SIZE) + PADDING_TOP, CELL_SIZE, CELL_SIZE) # Creates the grid's rectangles
            pygame.draw.rect(window, (0, 0, 0), rect, 1)  # Draw grid lines

            if grid[row][col] == 'player':
                pygame.draw.rect(window, PLAYER_COLOUR, rect)  # Draw player's square
            elif grid[row][col] == 'ai':
                pygame.draw.rect(window, AI_COLOUR, rect)  # Draw AI's square

    pygame.display.update()

def is_valid_move(row, col):
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] is None # Check if the move is valid

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

def ai_make_move():
    # AI's move (intelligent placement)

    # Check if AI can win
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if is_valid_move(row, col):
                grid[row][col] = 'ai'
                if check_winner() == 'ai':
                    grid[row][col] = 'ai'
                    ai_sound.play()  # Play the AI move sound
                    return
                grid[row][col] = None

    # Check if AI can block player's line of 4
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if is_valid_move(row, col):
                grid[row][col] = 'player'
                if check_winner() == 'player':
                    grid[row][col] = 'ai'
                    ai_sound.play()  # Play the AI move sound
                    return
                grid[row][col] = None

    # Otherwise, evaluate the best move as before
    best_move = None
    best_score = float('-inf')

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if is_valid_move(row, col):
                score = evaluate_move(row, col, 'ai', 'player', blocking=True)
                if score > best_score:
                    best_move = (row, col)
                    best_score = score

    if best_move is not None:
        row, col = best_move
        grid[row][col] = 'ai'
        ai_sound.play()  # Play the AI move sound

def evaluate_move(row, col, player, opponent, blocking=False):
    score = 0

    # Check horizontal line
    for c in range(col - 3, col + 1):
        if c >= 0 and c + 4 < GRID_SIZE:
            tiles = [grid[row][c+i] for i in range(5)]
            if tiles.count(opponent) == 4:
                if blocking:
                    # Block the player's line of 4 by placing a tile in the direction of the line of 3
                    if c - 1 >= 0 and grid[row][c - 1] is None:
                        score += 10
                    elif c + 5 < GRID_SIZE and grid[row][c + 5] is None:
                        score += 10

    # Check vertical line
    for r in range(row - 3, row + 1):
        if r >= 0 and r + 4 < GRID_SIZE:
            tiles = [grid[r+i][col] for i in range(5)]
            if tiles.count(opponent) == 4:
                if blocking:
                    # Block the player's line of 4 by placing a tile in the direction of the line of 3
                    if r - 1 >= 0 and grid[r - 1][col] is None:
                        score += 10
                    elif r + 5 < GRID_SIZE and grid[r + 5][col] is None:
                        score += 10

    # Check diagonal line (top-left to bottom-right)
    for i in range(5):
        r = row - i
        c = col - i
        if r >= 0 and c >= 0 and r + 4 < GRID_SIZE and c + 4 < GRID_SIZE:
            tiles = [grid[r+i][c+i] for i in range(5)]
            if tiles.count(opponent) == 4:
                if blocking:
                    # Block the player's line of 4 by placing a tile in the direction of the line of 3
                    if r - 1 >= 0 and c - 1 >= 0 and grid[r - 1][c - 1] is None:
                        score += 10
                    elif r + 5 < GRID_SIZE and c + 5 < GRID_SIZE and grid[r + 5][c + 5] is None:
                        score += 10

    # Check diagonal line (top-right to bottom-left)
    for i in range(5):
        r = row - i
        c = col + i
        if r >= 0 and c < GRID_SIZE and r + 4 < GRID_SIZE and c - 4 >= 0:
            tiles = [grid[r+i][c-i] for i in range(5)]
            if tiles.count(opponent) == 4:
                if blocking:
                    # Block the player's line of 4 by placing a tile in the direction of the line of 3
                    if r - 1 >= 0 and c + 1 < GRID_SIZE and grid[r - 1][c + 1] is None:
                        score += 10
                    elif r + 5 < GRID_SIZE and c - 5 >= 0 and grid[r + 5][c - 5] is None:
                        score += 10

    return score

def minimax(depth, maximizing_player):
    if depth == 0 or check_winner():
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if is_valid_move(row, col):
                    grid[row][col] = 'ai'
                    eval = minimax(depth - 1, False)
                    grid[row][col] = None
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if is_valid_move(row, col):
                    grid[row][col] = 'player'
                    eval = minimax(depth - 1, True)
                    grid[row][col] = None
                    min_eval = min(min_eval, eval)
        return min_eval

def display_winner(winner):
    global winner_sound_played

    if winner == 'player':
        text = custom_font.render("Player wins!", True, FONT_COLOUR)
    elif winner == 'ai':
        text = custom_font.render("AI wins!", True, FONT_COLOUR)
    else:
        text = custom_font.render("It's a tie!", True, FONT_COLOUR)

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

while True:
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

            if current_player == 'ai' and not game_over:
                ai_make_move()
                winner = check_winner()
                if winner is not None:
                    game_over = True

                current_player = 'player'

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'player' and not game_over:
                # Player's move
                mouse_pos = pygame.mouse.get_pos()
                row = (mouse_pos[1] - PADDING_TOP) // CELL_SIZE
                col = mouse_pos[0] // CELL_SIZE

                if is_valid_move(row, col):
                    grid[row][col] = 'player'
                    winner = check_winner()
                    if winner is not None:
                        game_over = True

                    current_player = 'ai'
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

        display_winner(winner) # Display the winner
        text = custom_font.render("Press 'R' to play again", True, FONT_COLOUR_2) # Display the restart message
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] - (PADDING_TOP // 2))) # Center the text
        window.blit(text, text_rect) # Display the text
        pygame.display.update() # Update the display

