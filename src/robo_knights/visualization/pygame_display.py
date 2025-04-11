import pygame
import sys
import random

# Constants for the display
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GRAY_COLOR = (128, 128, 128)
LIGHT_BROWN = (238, 238, 210)
DARK_BROWN = (118, 150, 86)

TILE_SIZE = 60
MARGIN = 20
SCREEN_SIZE = 8 * TILE_SIZE + 2 * MARGIN

# Example two-letter labels (instead of Unicode)
PIECE_LABELS = {
    'P': 'Wp', 'N': 'WN', 'B': 'WB', 'R': 'WR', 'Q': 'WQ', 'K': 'WK',
    'p': 'Bp', 'n': 'BN', 'b': 'BB', 'r': 'BR', 'q': 'BQ', 'k': 'BK'
}

def int_to_piece(val):
    """
    Convert an integer value to a piece symbol.
    
    Args:
        val (int): Integer value representing a piece
        
    Returns:
        str: Piece symbol
    """
    mapping = {
        1:'P',2:'N',3:'B',4:'R',5:'Q',6:'K',
        -1:'p',-2:'n',-3:'b',-4:'r',-5:'q',-6:'k'
    }
    return mapping.get(val,'.')

def draw_board(screen, board_state, font):
    """
    Draw the chess board and pieces.
    
    Args:
        screen: Pygame screen object
        board_state (numpy.ndarray): Current state of the board
        font: Pygame font object
    """
    for row in range(8):
        for col in range(8):
            # Chess coloring
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(
                screen, 
                color, 
                (MARGIN + col*TILE_SIZE, MARGIN + row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
            
            piece_val = board_state[row, col]
            if piece_val != 0:
                symbol = int_to_piece(piece_val)
                label = PIECE_LABELS.get(symbol, '')
                text_surface = font.render(label, True, BLACK_COLOR)
                text_rect = text_surface.get_rect(center=(
                    MARGIN + col*TILE_SIZE + TILE_SIZE//2,
                    MARGIN + row*TILE_SIZE + TILE_SIZE//2
                ))
                screen.blit(text_surface, text_rect)

def play_match(agent1, agent2, env):
    """
    Play a match between two agents and display it using Pygame.
    
    Args:
        agent1: First chess agent
        agent2: Second chess agent
        env: Chess environment
    """
    state = env.reset()
    done = False
    turn_white = True
    
    pygame.init()
    font = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("RL Chess Match")
    clock = pygame.time.Clock()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(GRAY_COLOR)
        draw_board(screen, state, font)
        pygame.display.flip()
        clock.tick(1)  # 1 move/sec
        
        legal_moves = env.get_legal_moves()
        if turn_white:
            move = agent1.select_action(state, legal_moves)
        else:
            move = agent2.select_action(state, legal_moves)
        
        if move not in legal_moves:
            move = random.choice(legal_moves)
        
        next_state, reward, done = env.step(move)
        state = next_state
        turn_white = not turn_white
    
    # Final board
    draw_board(screen, state, font)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit() 