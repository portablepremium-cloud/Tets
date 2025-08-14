import os
import sys

class ChessPiece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type
        self.color = color  # 'white' or 'black'
        self.position = position
        self.has_moved = False
        
    def get_symbol(self):
        """Get the Unicode symbol for the piece"""
        symbols = {
            'white': {
                'king': '♔', 'queen': '♕', 'rook': '♖', 
                'bishop': '♗', 'knight': '♘', 'pawn': '♙'
            },
            'black': {
                'king': '♚', 'queen': '♛', 'rook': '♜', 
                'bishop': '♝', 'knight': '♞', 'pawn': '♟'
            }
        }
        return symbols[self.color][self.piece_type]
        
    def get_valid_moves(self, board):
        """Get all valid moves for this piece"""
        moves = []
        row, col = self.position
        
        if self.piece_type == 'pawn':
            moves = self._get_pawn_moves(board)
        elif self.piece_type == 'rook':
            moves = self._get_rook_moves(board)
        elif self.piece_type == 'knight':
            moves = self._get_knight_moves(board)
        elif self.piece_type == 'bishop':
            moves = self._get_bishop_moves(board)
        elif self.piece_type == 'queen':
            moves = self._get_queen_moves(board)
        elif self.piece_type == 'king':
            moves = self._get_king_moves(board)
            
        return moves
    
    def _get_pawn_moves(self, board):
        moves = []
        row, col = self.position
        direction = -1 if self.color == 'white' else 1
        
        # Forward move
        new_row = row + direction
        if 0 <= new_row < 8 and board[new_row][col] is None:
            moves.append((new_row, col))
            
            # Double move from starting position
            if not self.has_moved:
                new_row2 = row + 2 * direction
                if 0 <= new_row2 < 8 and board[new_row2][col] is None:
                    moves.append((new_row2, col))
        
        # Diagonal captures
        for dcol in [-1, 1]:
            new_col = col + dcol
            new_row = row + direction
            if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                board[new_row][new_col] is not None and 
                board[new_row][new_col].color != self.color):
                moves.append((new_row, new_col))
        
        return moves
    
    def _get_rook_moves(self, board):
        moves = []
        row, col = self.position
        
        # Horizontal and vertical directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                    
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def _get_knight_moves(self, board):
        moves = []
        row, col = self.position
        
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for drow, dcol in knight_moves:
            new_row, new_col = row + drow, col + dcol
            if (0 <= new_row < 8 and 0 <= new_col < 8 and
                (board[new_row][new_col] is None or 
                 board[new_row][new_col].color != self.color)):
                moves.append((new_row, new_col))
        
        return moves
    
    def _get_bishop_moves(self, board):
        moves = []
        row, col = self.position
        
        # Diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for drow, dcol in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * drow, col + i * dcol
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                    
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def _get_queen_moves(self, board):
        # Queen combines rook and bishop moves
        return self._get_rook_moves(board) + self._get_bishop_moves(board)
    
    def _get_king_moves(self, board):
        moves = []
        row, col = self.position
        
        # All 8 directions around the king
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if (0 <= new_row < 8 and 0 <= new_col < 8 and
                (board[new_row][new_col] is None or 
                 board[new_row][new_col].color != self.color)):
                moves.append((new_row, new_col))
        
        return moves

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.game_over = False
        self.winner = None
        self._initialize_board()
    
    def _initialize_board(self):
        # Set up pawns
        for col in range(8):
            self.board[1][col] = ChessPiece('pawn', 'black', (1, col))
            self.board[6][col] = ChessPiece('pawn', 'white', (6, col))
        
        # Set up other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        
        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = ChessPiece(piece_type, 'black', (0, col))
            self.board[7][col] = ChessPiece(piece_type, 'white', (7, col))
    
    def get_piece_at(self, position):
        row, col = position
        return self.board[row][col]
    
    def is_valid_move(self, start_pos, end_pos):
        """Check if a move is valid"""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Check if start position has a piece
        piece = self.board[start_row][start_col]
        if piece is None or piece.color != self.current_player:
            return False
        
        # Get valid moves for the piece
        valid_moves = piece.get_valid_moves(self.board)
        return (end_row, end_col) in valid_moves
    
    def make_move(self, start_pos, end_pos):
        """Make a move on the board"""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        piece = self.board[start_row][start_col]
        if piece is None:
            return False
        
        # Check if move is valid
        if not self.is_valid_move(start_pos, end_pos):
            return False
        
        # Check for pawn promotion
        if (piece.piece_type == 'pawn' and 
            ((piece.color == 'white' and end_row == 0) or 
             (piece.color == 'black' and end_row == 7))):
            piece.piece_type = 'queen'
        
        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        piece.position = (end_row, end_col)
        piece.has_moved = True
        
        # Check for checkmate or stalemate
        self._check_game_end()
        
        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        return True
    
    def _check_game_end(self):
        """Check if the game is over (checkmate or stalemate)"""
        # Simple implementation - check if current player has any valid moves
        has_moves = False
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    if piece.get_valid_moves(self.board):
                        has_moves = True
                        break
            if has_moves:
                break
        
        if not has_moves:
            self.game_over = True
            # Determine winner (opposite of current player)
            self.winner = 'black' if self.current_player == 'white' else 'white'
    
    def display(self):
        """Display the chess board in the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("  " + "=" * 50)
        print(f"  Chess Game - Current Player: {self.current_player.title()}")
        print("  " + "=" * 50)
        print()
        
        # Column labels
        print("     a   b   c   d   e   f   g   h")
        print("   +---+---+---+---+---+---+---+---+")
        
        for row in range(8):
            print(f" {8-row} |", end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(f"{piece.get_symbol()} |", end=" ")
                else:
                    # Alternate colors for empty squares
                    if (row + col) % 2 == 0:
                        print("  |", end=" ")
                    else:
                        print("██|", end=" ")
            print(f" {8-row}")
            if row < 7:
                print("   +---+---+---+---+---+---+---+---+")
        
        print("   +---+---+---+---+---+---+---+---+")
        print("     a   b   c   d   e   f   g   h")
        print()
        
        if self.game_over:
            print(f"  Game Over! {self.winner.title()} wins!")
        else:
            print("  Enter moves in format: e2e4 (from square to square)")
            print("  Type 'quit' to exit, 'reset' to start new game")

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
    
    def parse_move(self, move_str):
        """Parse a move string like 'e2e4' into coordinates"""
        if len(move_str) != 4:
            return None, None
        
        try:
            from_col = ord(move_str[0].lower()) - ord('a')
            from_row = 8 - int(move_str[1])
            to_col = ord(move_str[2].lower()) - ord('a')
            to_row = 8 - int(move_str[3])
            
            if (0 <= from_row < 8 and 0 <= from_col < 8 and 
                0 <= to_row < 8 and 0 <= to_col < 8):
                return (from_row, from_col), (to_row, to_col)
        except (ValueError, IndexError):
            pass
        
        return None, None
    
    def run(self):
        """Main game loop"""
        print("Welcome to Chess!")
        print("Type 'help' for instructions")
        
        while True:
            self.board.display()
            
            if self.board.game_over:
                break
            
            move = input(f"\n{self.board.current_player.title()}'s move: ").strip().lower()
            
            if move == 'quit':
                print("Thanks for playing!")
                break
            elif move == 'reset':
                self.board = ChessBoard()
                continue
            elif move == 'help':
                print("\nChess Move Instructions:")
                print("- Enter moves in format: e2e4")
                print("- First two characters: starting square (e.g., e2)")
                print("- Last two characters: ending square (e.g., e4)")
                print("- Commands: quit, reset, help")
                input("Press Enter to continue...")
                continue
            
            start_pos, end_pos = self.parse_move(move)
            
            if start_pos is None or end_pos is None:
                print("Invalid move format. Use format like 'e2e4'")
                input("Press Enter to continue...")
                continue
            
            if not self.board.make_move(start_pos, end_pos):
                print("Invalid move!")
                input("Press Enter to continue...")
                continue
        
        print("Game ended.")

if __name__ == "__main__":
    game = ChessGame()
    game.run()