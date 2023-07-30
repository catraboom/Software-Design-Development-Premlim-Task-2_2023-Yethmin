# Game constants
GRID_SIZE = 11 # Number of rows and columns
EMPTY_CELL = '-' # Empty cell
PLAYER_CELL = 'X' # Player's cell
AI_CELL = 'O' # AI's cell

# Create the grid
grid = [[EMPTY_CELL] * GRID_SIZE for _ in range(GRID_SIZE)]

def draw_grid(): # Draw the grid
    for row in range(GRID_SIZE): 
        for col in range(GRID_SIZE): 
            print(grid[row][col], end=' ')
        print()

def is_valid_move(row, col): # Check if the move is valid
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] == EMPTY_CELL

def check_winner(): # Check if there is a winner
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != EMPTY_CELL:
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

def alpha_beta_pruning(row, col, depth, maximizing_player, alpha, beta):
    if depth == 0 or row >= GRID_SIZE or col >= GRID_SIZE:
        return evaluate_move(row, col, AI_CELL) - evaluate_move(row, col, PLAYER_CELL)

    if maximizing_player:
        max_eval = float("-inf")
        for r in range(row, row + 4):
            for c in range(col, col + 4):
                if is_valid_move(r, c):
                    grid[r][c] = AI_CELL
                    eval = alpha_beta_pruning(r, c, depth - 1, False, alpha, beta)
                    grid[r][c] = EMPTY_CELL
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float("inf")
        for r in range(row, row + 4):
            for c in range(col, col + 4):
                if is_valid_move(r, c):
                    grid[r][c] = PLAYER_CELL
                    eval = alpha_beta_pruning(r, c, depth - 1, True, alpha, beta)
                    grid[r][c] = EMPTY_CELL
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def ai_make_move():
    # AI's move (intelligent placement)
    best_move = None
    best_score = float("-inf")
    depth = 4  # Adjust the depth of the search based on performance and desired difficulty

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if is_valid_move(row, col):
                grid[row][col] = AI_CELL
                score = alpha_beta_pruning(row, col, depth - 1, False, float("-inf"), float("inf"))
                grid[row][col] = EMPTY_CELL

                if score > best_score:
                    best_move = (row, col)
                    best_score = score

    if best_move is not None:
        row, col = best_move
        grid[row][col] = AI_CELL

def evaluate_move(row, col, player, blocking=False):
    score = 0

    # Check horizontal line
    for c in range(col, col + 4):
        if c < GRID_SIZE:
            if grid[row][c] == player:
                score += 1
            elif grid[row][c] != EMPTY_CELL:
                score -= 1
            elif blocking and grid[row][c] != PLAYER_CELL:
                score += 0.5

    # Check vertical line
    for r in range(row, row + 4):
        if r < GRID_SIZE:
            if grid[r][col] == player:
                score += 1
            elif grid[r][col] != EMPTY_CELL:
                score -= 1
            elif blocking and grid[r][col] != PLAYER_CELL:
                score += 0.5

    # Check diagonal line (top-left to bottom-right)
    for i in range(4):
        r = row + i
        c = col + i
        if r < GRID_SIZE and c < GRID_SIZE:
            if grid[r][c] == player:
                score += 1
            elif grid[r][c] != EMPTY_CELL:
                score -= 1
            elif blocking and grid[r][c] != PLAYER_CELL:
                score += 0.5

    # Check diagonal line (top-right to bottom-left)
    for i in range(4):
        r = row + i
        c = col - i
        if r < GRID_SIZE and c >= 0:
            if grid[r][c] == player:
                score += 1
            elif grid[r][c] != EMPTY_CELL:
                score -= 1
            elif blocking and grid[r][c] != PLAYER_CELL:
                score += 0.5

    return score

def display_winner(winner): # Display the winner
    if winner == PLAYER_CELL:
        print("Player wins!")
    elif winner == AI_CELL:
        print("AI wins!")
    else:
        print("It's a tie!")

def reset_game():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = EMPTY_CELL

# Game loop
restart_game = False
current_player = PLAYER_CELL

while True: 
    if restart_game:
        reset_game()
        restart_game = False
        current_player = PLAYER_CELL

    game_over = False
    winner = None

    while not game_over: 
        draw_grid()

        if current_player == AI_CELL: 
            ai_make_move()
            winner = check_winner()
            if winner is not None:
                game_over = True
            current_player = PLAYER_CELL
        else:
            while True:
                try:
                    print("Player's move (row col):")
                    row, col = map(int, input().split())
                    if is_valid_move(row, col):
                        grid[row][col] = PLAYER_CELL
                        winner = check_winner()
                        if winner is not None:
                            game_over = True
                        current_player = AI_CELL
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")

    draw_grid()

    # Game over loop
    while True:
        print("Game over.")
        display_winner(winner)
        print("Press 'R' to play again")
        choice = input()
        if choice.lower() == 'r':
            restart_game = True
            break
