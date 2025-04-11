"""
Chess visualization utilities.
"""

import pygame
import chess
import os
from pathlib import Path

class ChessVisualizer:
    """A class for visualizing chess games using pygame."""
    
    def __init__(self, window_size=800):
        """Initialize the visualizer.
        
        Args:
            window_size (int): Size of the window in pixels
        """
        pygame.init()
        self.window_size = window_size
        self.square_size = window_size // 8
        self.screen = pygame.display.set_mode((window_size, window_size))
        pygame.display.set_caption("Chess Game")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.HIGHLIGHT = (255, 255, 0, 128)
        
        # Load pieces
        self.pieces = self._load_pieces()
    
    def _load_pieces(self):
        """Load chess piece images."""
        pieces = {}
        piece_names = ['p', 'n', 'b', 'r', 'q', 'k']
        colors = ['b', 'w']
        
        for color in colors:
            for piece in piece_names:
                name = f"{color}{piece}"
                try:
                    # Try to load from pieces directory
                    if os.path.exists("pieces"):
                        img = pygame.image.load(f"pieces/{name}.png")
                    else:
                        # Create placeholder
                        img = pygame.Surface((self.square_size, self.square_size))
                        img.fill(self.GRAY)
                        font = pygame.font.SysFont(None, 36)
                        text = font.render(name, True, self.WHITE if color == 'w' else self.BLACK)
                        text_rect = text.get_rect(center=(self.square_size/2, self.square_size/2))
                        img.blit(text, text_rect)
                    
                    pieces[name] = pygame.transform.scale(img, (self.square_size, self.square_size))
                except Exception as e:
                    print(f"Error loading {name}: {e}")
                    # Create placeholder
                    img = pygame.Surface((self.square_size, self.square_size))
                    img.fill(self.GRAY)
                    font = pygame.font.SysFont(None, 36)
                    text = font.render(name, True, self.WHITE if color == 'w' else self.BLACK)
                    text_rect = text.get_rect(center=(self.square_size/2, self.square_size/2))
                    img.blit(text, text_rect)
                    pieces[name] = img
        
        return pieces
    
    def draw_board(self, board, selected_square=None):
        """Draw the chess board and pieces.
        
        Args:
            board (chess.Board): The chess board to draw
            selected_square (int, optional): The selected square to highlight
        """
        self.screen.fill(self.WHITE)
        
        # Draw board squares
        for rank in range(8):
            for file in range(8):
                color = self.WHITE if (rank + file) % 2 == 0 else self.GRAY
                pygame.draw.rect(self.screen, color,
                               (file * self.square_size, rank * self.square_size,
                                self.square_size, self.square_size))
        
        # Highlight selected square
        if selected_square is not None:
            file = chess.square_file(selected_square)
            rank = chess.square_rank(selected_square)
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            s.fill(self.HIGHLIGHT)
            self.screen.blit(s, (file * self.square_size, rank * self.square_size))
        
        # Draw pieces
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                color = 'w' if piece.color else 'b'
                name = f"{color}{piece.symbol().lower()}"
                if name in self.pieces:
                    self.screen.blit(self.pieces[name],
                                   (file * self.square_size, rank * self.square_size))
        
        pygame.display.flip()
    
    def get_square_from_mouse(self, pos):
        """Convert mouse position to chess square.
        
        Args:
            pos (tuple): Mouse position (x, y)
            
        Returns:
            int: Chess square number or None if invalid
        """
        file = pos[0] // self.square_size
        rank = 7 - (pos[1] // self.square_size)  # Flip rank for chess notation
        if 0 <= file <= 7 and 0 <= rank <= 7:
            return chess.square(file, rank)
        return None
    
    def close(self):
        """Close the pygame window."""
        pygame.quit() 