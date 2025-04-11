import chess
import numpy as np

class ChessEnv:
    """
    Chess environment for reinforcement learning.
    Wraps the chess library to provide a gym-like interface.
    """
    def __init__(self):
        self.board = chess.Board()
        
    def reset(self):
        """Reset the environment to the initial state."""
        self.board.reset()
        return self.get_state()
    
    def get_state(self):
        """
        Get the current state of the board as a numpy array.
        
        Returns:
            numpy.ndarray: A flattened representation of the board
        """
        # Create a 8x8x12 array (one plane per piece type and color)
        state = np.zeros((8, 8, 12), dtype=np.float32)
        
        # Fill the state array based on the current board
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                # Calculate the plane index (0-11)
                # 6 piece types * 2 colors = 12 planes
                plane_idx = piece.piece_type - 1 + (0 if piece.color else 6)
                rank, file = divmod(square, 8)
                state[rank, file, plane_idx] = 1.0
        
        return state
    
    def step(self, action):
        """
        Take a step in the environment.
        
        Args:
            action (chess.Move): The move to make
            
        Returns:
            tuple: (next_state, reward, done, info)
        """
        if action not in self.board.legal_moves:
            return self.get_state(), -1.0, True, {"error": "Illegal move"}
        
        # Make the move
        self.board.push(action)
        
        # Get the new state
        next_state = self.get_state()
        
        # Calculate reward
        reward = self._calculate_reward()
        
        # Check if the game is over
        done = self.is_game_over()
        
        info = {
            "fen": self.board.fen(),
            "is_check": self.board.is_check(),
            "is_checkmate": self.board.is_checkmate(),
            "is_stalemate": self.board.is_stalemate(),
            "is_insufficient_material": self.board.is_insufficient_material(),
            "legal_moves": [move.uci() for move in self.board.legal_moves]
        }
        
        return next_state, reward, done, info
    
    def _calculate_reward(self):
        """
        Calculate the reward for the current state.
        
        Returns:
            float: The reward value
        """
        # Simple reward based on material difference
        if self.board.is_game_over():
            if self.board.is_checkmate():
                # Checkmate: +1 for white win, -1 for black win
                return 1.0 if self.board.turn == chess.BLACK else -1.0
            else:
                # Draw: 0 reward
                return 0.0
        
        # Material-based reward
        material_value = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        white_material = sum(material_value[piece.piece_type] 
                            for piece in self.board.piece_map().values() 
                            if piece.color == chess.WHITE)
        
        black_material = sum(material_value[piece.piece_type] 
                            for piece in self.board.piece_map().values() 
                            if piece.color == chess.BLACK)
        
        # Normalize the material difference
        material_diff = (white_material - black_material) / 100.0
        
        return material_diff
    
    def get_legal_moves(self):
        """
        Get a list of legal moves.
        
        Returns:
            list: List of legal chess.Move objects
        """
        return list(self.board.legal_moves)
    
    def is_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.board.is_game_over() 