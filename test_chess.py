#!/usr/bin/env python3
"""
Test script for the chess game logic.
This script tests basic chess piece movements and game functionality.
"""

import sys
import os

# Import the chess classes from the terminal version
from chess_terminal import ChessPiece, ChessBoard

def test_pawn_movement():
    """Test pawn movement logic"""
    print("Testing pawn movement...")
    
    # Create a test board
    board = [[None for _ in range(8)] for _ in range(8)]
    
    # Test white pawn
    white_pawn = ChessPiece('pawn', 'white', (6, 3))  # d2
    board[6][3] = white_pawn
    
    moves = white_pawn.get_valid_moves(board)
    expected_moves = [(5, 3), (4, 3)]  # d3, d4
    
    if set(moves) == set(expected_moves):
        print("✓ White pawn movement test passed")
    else:
        print(f"✗ White pawn movement test failed. Expected {expected_moves}, got {moves}")
    
    # Test black pawn
    black_pawn = ChessPiece('pawn', 'black', (1, 4))  # e7
    board[1][4] = black_pawn
    
    moves = black_pawn.get_valid_moves(board)
    expected_moves = [(2, 4), (3, 4)]  # e6, e5
    
    if set(moves) == set(expected_moves):
        print("✓ Black pawn movement test passed")
    else:
        print(f"✗ Black pawn movement test failed. Expected {expected_moves}, got {moves}")

def test_knight_movement():
    """Test knight movement logic"""
    print("\nTesting knight movement...")
    
    board = [[None for _ in range(8)] for _ in range(8)]
    knight = ChessPiece('knight', 'white', (4, 4))  # e4
    board[4][4] = knight
    
    moves = knight.get_valid_moves(board)
    expected_moves = [
        (2, 3), (2, 5),  # c3, g3
        (3, 2), (3, 6),  # d2, f2
        (5, 2), (5, 6),  # d6, f6
        (6, 3), (6, 5)   # c5, g5
    ]
    
    if set(moves) == set(expected_moves):
        print("✓ Knight movement test passed")
    else:
        print(f"✗ Knight movement test failed. Expected {expected_moves}, got {moves}")

def test_rook_movement():
    """Test rook movement logic"""
    print("\nTesting rook movement...")
    
    board = [[None for _ in range(8)] for _ in range(8)]
    rook = ChessPiece('rook', 'white', (4, 4))  # e4
    board[4][4] = rook
    
    # Add an enemy piece to test capture
    enemy_pawn = ChessPiece('pawn', 'black', (4, 6))  # f4
    board[4][6] = enemy_pawn
    
    moves = rook.get_valid_moves(board)
    
    # Should be able to move in all directions except blocked by enemy piece
    # Should include the enemy piece position (capture)
    if (4, 6) in moves:
        print("✓ Rook capture test passed")
    else:
        print("✗ Rook capture test failed")

def test_queen_movement():
    """Test queen movement logic"""
    print("\nTesting queen movement...")
    
    board = [[None for _ in range(8)] for _ in range(8)]
    queen = ChessPiece('queen', 'white', (4, 4))  # e4
    board[4][4] = queen
    
    moves = queen.get_valid_moves(board)
    
    # Queen should have many valid moves (combines rook and bishop)
    if len(moves) > 20:  # Queen typically has 27 moves from center
        print("✓ Queen movement test passed")
    else:
        print(f"✗ Queen movement test failed. Expected many moves, got {len(moves)}")

def test_king_movement():
    """Test king movement logic"""
    print("\nTesting king movement...")
    
    board = [[None for _ in range(8)] for _ in range(8)]
    king = ChessPiece('king', 'white', (4, 4))  # e4
    board[4][4] = king
    
    moves = king.get_valid_moves(board)
    expected_moves = [
        (3, 3), (3, 4), (3, 5),  # d3, e3, f3
        (4, 3), (4, 5),          # d4, f4
        (5, 3), (5, 4), (5, 5)   # d5, e5, f5
    ]
    
    if set(moves) == set(expected_moves):
        print("✓ King movement test passed")
    else:
        print(f"✗ King movement test failed. Expected {expected_moves}, got {moves}")

def test_board_initialization():
    """Test chess board initialization"""
    print("\nTesting board initialization...")
    
    chess_board = ChessBoard()
    
    # Check that pieces are in correct starting positions
    # White pawns should be on row 6
    for col in range(8):
        piece = chess_board.board[6][col]
        if piece and piece.piece_type == 'pawn' and piece.color == 'white':
            continue
        else:
            print(f"✗ White pawn test failed at column {col}")
            return
    
    # Black pawns should be on row 1
    for col in range(8):
        piece = chess_board.board[1][col]
        if piece and piece.piece_type == 'pawn' and piece.color == 'black':
            continue
        else:
            print(f"✗ Black pawn test failed at column {col}")
            return
    
    # Check back row pieces
    piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    
    for col, piece_type in enumerate(piece_order):
        # White back row
        piece = chess_board.board[7][col]
        if piece and piece.piece_type == piece_type and piece.color == 'white':
            continue
        else:
            print(f"✗ White back row test failed at column {col}")
            return
        
        # Black back row
        piece = chess_board.board[0][col]
        if piece and piece.piece_type == piece_type and piece.color == 'black':
            continue
        else:
            print(f"✗ Black back row test failed at column {col}")
            return
    
    print("✓ Board initialization test passed")

def test_move_validation():
    """Test move validation"""
    print("\nTesting move validation...")
    
    chess_board = ChessBoard()
    
    # Test valid move
    if chess_board.is_valid_move((6, 4), (4, 4)):  # e2e4
        print("✓ Valid move test passed")
    else:
        print("✗ Valid move test failed")
    
    # Test invalid move (wrong player)
    if not chess_board.is_valid_move((1, 4), (3, 4)):  # Black's turn but trying to move white
        print("✓ Invalid move (wrong player) test passed")
    else:
        print("✗ Invalid move (wrong player) test failed")
    
    # Test invalid move (no piece)
    if not chess_board.is_valid_move((3, 3), (4, 4)):  # Empty square
        print("✓ Invalid move (no piece) test passed")
    else:
        print("✗ Invalid move (no piece) test failed")

def test_pawn_promotion():
    """Test pawn promotion"""
    print("\nTesting pawn promotion...")
    
    chess_board = ChessBoard()
    
    # Clear the board and set up a pawn near promotion (has already moved)
    chess_board.board = [[None for _ in range(8)] for _ in range(8)]
    pawn = ChessPiece('pawn', 'white', (1, 0))  # a7
    pawn.has_moved = True  # Mark as already moved
    chess_board.board[1][0] = pawn
    chess_board.current_player = 'white'
    
    # Move pawn to promotion square
    if chess_board.make_move((1, 0), (0, 0)):  # a7a8
        promoted_piece = chess_board.board[0][0]
        if promoted_piece and promoted_piece.piece_type == 'queen':
            print("✓ Pawn promotion test passed")
        else:
            print("✗ Pawn promotion test failed")
    else:
        print("✗ Pawn promotion move failed")

def run_all_tests():
    """Run all tests"""
    print("Running Chess Game Tests")
    print("=" * 40)
    
    test_pawn_movement()
    test_knight_movement()
    test_rook_movement()
    test_queen_movement()
    test_king_movement()
    test_board_initialization()
    test_move_validation()
    test_pawn_promotion()
    
    print("\n" + "=" * 40)
    print("All tests completed!")

if __name__ == "__main__":
    run_all_tests()