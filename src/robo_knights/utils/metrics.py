"""
Metrics tracking utilities.
"""

import json
from pathlib import Path
from datetime import datetime

class MetricsTracker:
    """A class for tracking and logging game metrics."""
    
    def __init__(self, log_dir="logs"):
        """Initialize the metrics tracker.
        
        Args:
            log_dir (str): Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.current_game = {
            "moves": [],
            "start_time": None,
            "end_time": None,
            "winner": None,
            "total_moves": 0,
            "game_duration": None
        }
    
    def start_game(self):
        """Start tracking a new game."""
        self.current_game = {
            "moves": [],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "winner": None,
            "total_moves": 0,
            "game_duration": None
        }
    
    def log_move(self, move, board):
        """Log a move and the resulting board state.
        
        Args:
            move (chess.Move): The move that was made
            board (chess.Board): The board after the move
        """
        self.current_game["moves"].append({
            "move": move.uci(),
            "timestamp": datetime.now().isoformat(),
            "fen": board.fen(),
            "is_check": board.is_check(),
            "is_checkmate": board.is_checkmate(),
            "is_stalemate": board.is_stalemate(),
            "is_insufficient_material": board.is_insufficient_material(),
            "is_game_over": board.is_game_over()
        })
        self.current_game["total_moves"] = len(self.current_game["moves"])
    
    def end_game(self, winner=None):
        """End the current game and save metrics.
        
        Args:
            winner (str, optional): The winner of the game ('white', 'black', or None for draw)
        """
        self.current_game["end_time"] = datetime.now().isoformat()
        self.current_game["winner"] = winner
        
        # Calculate game duration
        if self.current_game["start_time"]:
            start = datetime.fromisoformat(self.current_game["start_time"])
            end = datetime.fromisoformat(self.current_game["end_time"])
            self.current_game["game_duration"] = str(end - start)
        
        
    
    def get_current_metrics(self):
        """Get the metrics for the current game.
        
        Returns:
            dict: Current game metrics
        """
        return self.current_game.copy()
    
    def get_move_history(self):
        """Get the move history for the current game.
        
        Returns:
            list: List of moves in UCI format
        """
        return [move["move"] for move in self.current_game["moves"]] 