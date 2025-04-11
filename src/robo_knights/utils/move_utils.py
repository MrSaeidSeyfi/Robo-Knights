import chess

def move_to_index(move):
    """
    Convert a chess move to a unique integer index.
    
    Args:
        move (chess.Move): The chess move to convert
        
    Returns:
        int: A unique integer index representing the move
    """
    promo_map = {None: 0, chess.QUEEN: 1, chess.ROOK: 2, chess.BISHOP: 3, chess.KNIGHT: 4}
    from_sq = move.from_square
    to_sq = move.to_square
    promotion = move.promotion if move.promotion in promo_map else None
    
    promo_idx = promo_map.get(promotion, 0)
    idx = from_sq * 64 * 5 + to_sq * 5 + promo_idx
    if idx < 0 or idx >= 64*64*5:
        return None
    return idx

def index_to_move(idx):
    """
    Convert a unique integer index back to a chess move.
    
    Args:
        idx (int): The integer index to convert
        
    Returns:
        chess.Move: The corresponding chess move
    """
    if idx < 0 or idx >= 64*64*5:
        return None
    promo_idx = idx % 5
    idx //= 5
    to_sq = idx % 64
    idx //= 64
    from_sq = idx
    promo_map_inv = {0: None, 1: chess.QUEEN, 2: chess.ROOK, 3: chess.BISHOP, 4: chess.KNIGHT}
    promotion = promo_map_inv[promo_idx]
    return chess.Move(from_sq, to_sq, promotion=promotion) 