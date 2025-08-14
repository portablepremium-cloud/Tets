#!/usr/bin/env python3
"""
Demo script for the chess game.
This script demonstrates a few sample moves and shows the game in action.
"""

from chess_terminal import ChessBoard

def demo_chess_game():
    """Demonstrate the chess game with some sample moves"""
    print("Chess Game Demo")
    print("=" * 50)
    
    # Create a new chess board
    board = ChessBoard()
    
    # Show initial board
    print("\nInitial board setup:")
    board.display()
    
    # Demo some moves
    moves = [
        ("e2e4", "White moves pawn from e2 to e4"),
        ("e7e5", "Black moves pawn from e7 to e5"),
        ("g1f3", "White moves knight from g1 to f3"),
        ("b8c6", "Black moves knight from b8 to c6"),
        ("f1c4", "White moves bishop from f1 to c4"),
        ("f8c5", "Black moves bishop from f8 to c5"),
        ("e1g1", "White castles kingside (simplified)"),
    ]
    
    for move_str, description in moves:
        print(f"\n{description}")
        print(f"Move: {move_str}")
        
        # Parse the move
        from_pos = (8 - int(move_str[1]), ord(move_str[0].lower()) - ord('a'))
        to_pos = (8 - int(move_str[3]), ord(move_str[2].lower()) - ord('a'))
        
        # Make the move
        if board.make_move(from_pos, to_pos):
            print("✓ Move successful!")
        else:
            print("✗ Move failed!")
            break
        
        # Show the board after the move
        board.display()
        
        if board.game_over:
            print(f"Game Over! {board.winner.title()} wins!")
            break
    
    print("\nDemo completed!")

if __name__ == "__main__":
    demo_chess_game()