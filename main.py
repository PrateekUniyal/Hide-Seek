import pygame
import sys

# Initialize Pygame
pygame.init()

# Define dimensions and colors
CELL_SIZE = 100  # Size of each cell
ROWS, COLS = 6, 6
BOARD_WIDTH = CELL_SIZE * COLS
BOARD_HEIGHT = CELL_SIZE * ROWS
LINE_COLOR = (255, 255, 255)  # White for better visibility
BACKGROUND_COLOR = (0, 0, 128)  # Dark blue for better contrast
BLACK_COLOR = (0, 0, 0)  # Black
WHITE_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (255, 255, 255)  # White

# Create the display surface
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT + 50))  # Extra space for the text
pygame.display.set_caption('6x6 Board with Movable Pieces')

# Initialize the font
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Load and play background music
pygame.mixer.init()
pygame.mixer.music.load('sound_Assets/smile.mp3')  # Replace with the path to your music file
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load victory music
victory_music = 'sound_Assets/celebration-short-version-170834.mp3'  # Replace with the path to your victory music file

# Initial positions of the pieces (in grid coordinates)
black_piece = {'x': 0, 'y': 0, 'color': BLACK_COLOR}
white_piece = {'x': 1, 'y': 1, 'color': WHITE_COLOR}
turn = 'white'  # White moves first
winner = None  # No winner initially
turn_start_time = None  # Start time of the turn
COUNTDOWN_TIME = 2000  # 2 seconds in milliseconds
first_move = True  # Flag to check if the first move has been made

def draw_board():
    for x in range(0, BOARD_WIDTH, CELL_SIZE):
        for y in range(0, BOARD_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

def draw_piece(piece):
    # Convert grid coordinates to pixel coordinates
    pixel_x = piece['x'] * CELL_SIZE + CELL_SIZE // 2
    pixel_y = piece['y'] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, piece['color'], (pixel_x, pixel_y), CELL_SIZE // 3)

def draw_turn_text():
    if winner:
        text = font.render(f"{winner.capitalize()} piece wins!", True, TEXT_COLOR)
    else:
        text = font.render(f"{turn.capitalize()}'s turn", True, TEXT_COLOR)
    screen.blit(text, (10, BOARD_HEIGHT + 10))

def draw_winner_circle():
    if winner == 'white':
        color = WHITE_COLOR
    else:
        color = BLACK_COLOR
    pixel_x = white_piece['x'] * CELL_SIZE + CELL_SIZE // 2
    pixel_y = white_piece['y'] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, color, (pixel_x, pixel_y), CELL_SIZE // 3)

def draw_countdown():
    elapsed_time = pygame.time.get_ticks() - turn_start_time
    remaining_time = max(0, COUNTDOWN_TIME - elapsed_time) // 1000  # Convert to seconds
    text = font.render(f"Next turn in: {remaining_time}", True, TEXT_COLOR)
    screen.blit(text, (BOARD_WIDTH - 200, BOARD_HEIGHT + 10))

def play_victory_music():
    pygame.mixer.music.stop()  # Stop the current background music
    pygame.mixer.music.load(victory_music)  # Load the victory music
    pygame.mixer.music.play()  # Play the victory music

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not winner:  # Only allow moves if no winner
            if first_move:
                piece = white_piece
            else:
                piece = white_piece if turn == 'white' else black_piece

            moved = False
            if event.key == pygame.K_LEFT and piece['x'] > 0:
                piece['x'] -= 1
                moved = True
            elif event.key == pygame.K_RIGHT and piece['x'] < COLS - 1:
                piece['x'] += 1
                moved = True
            elif event.key == pygame.K_UP and piece['y'] > 0:
                piece['y'] -= 1
                moved = True
            elif event.key == pygame.K_DOWN and piece['y'] < ROWS - 1:
                piece['y'] += 1
                moved = True

            if moved:
                # Check for win condition
                if black_piece['x'] == white_piece['x'] and black_piece['y'] == white_piece['y']:
                    winner = 'black' if turn == 'black' else 'white'
                    play_victory_music()  # Play the victory music

                # Alternate turns and reset the countdown
                turn = 'black' if turn == 'white' else 'white'
                turn_start_time = pygame.time.get_ticks()
                first_move = False

    screen.fill(BACKGROUND_COLOR)
    draw_board()

    if not winner:
        if first_move or (pygame.time.get_ticks() - turn_start_time) >= COUNTDOWN_TIME:
            if first_move or turn == 'white':
                draw_piece(white_piece)
            elif turn == 'black':
                draw_piece(black_piece)
        else:
            draw_countdown()
    else:
        # Draw both pieces if there's a winner so the final move is visible
        draw_piece(white_piece)
        draw_piece(black_piece)
        draw_winner_circle()

    draw_turn_text()
    pygame.display.flip()
