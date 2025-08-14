import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (222, 184, 135)
HIGHLIGHT = (255, 255, 0, 128)
MOVE_HINT = (0, 255, 0, 128)

# Colors for the board
BOARD_COLORS = [LIGHT_BROWN, BROWN]

class ChessPiece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type
        self.color = color  # 'white' or 'black'
        self.position = position
        self.has_moved = False
        
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
        self.selected_piece = None
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

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        self.board = ChessBoard()
        self.selected_square = None
        self.valid_moves = []
        
        # Load piece images (we'll create simple colored rectangles for now)
        self.piece_images = self._create_piece_images()
    
    def _create_piece_images(self):
        """Create simple piece representations"""
        images = {}
        piece_colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        
        for color in ['white', 'black']:
            for piece_type in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                # Create a simple surface for each piece
                surface = pygame.Surface((SQUARE_SIZE - 10, SQUARE_SIZE - 10))
                surface.fill(piece_colors[color])
                pygame.draw.rect(surface, (128, 128, 128), surface.get_rect(), 3)
                
                # Add text to identify piece type
                font = pygame.font.Font(None, 36)
                text = font.render(piece_type[0].upper(), True, 
                                 (255, 255, 255) if color == 'black' else (0, 0, 0))
                text_rect = text.get_rect(center=surface.get_rect().center)
                surface.blit(text, text_rect)
                
                images[f"{color}_{piece_type}"] = surface
        
        return images
    
    def draw_board(self):
        """Draw the chess board"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                color = BOARD_COLORS[(row + col) % 2]
                
                # Draw square
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight selected square
                if self.selected_square == (row, col):
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    highlight_surface.set_alpha(128)
                    highlight_surface.fill(HIGHLIGHT)
                    self.screen.blit(highlight_surface, (x, y))
                
                # Highlight valid moves
                if (row, col) in self.valid_moves:
                    move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    move_surface.set_alpha(128)
                    move_surface.fill(MOVE_HINT)
                    self.screen.blit(move_surface, (x, y))
                
                # Draw piece
                piece = self.board.get_piece_at((row, col))
                if piece:
                    piece_key = f"{piece.color}_{piece.piece_type}"
                    if piece_key in self.piece_images:
                        piece_surface = self.piece_images[piece_key]
                        piece_rect = piece_surface.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                        self.screen.blit(piece_surface, piece_rect)
    
    def get_square_from_pos(self, pos):
        """Convert mouse position to board coordinates"""
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return (row, col) if 0 <= row < 8 and 0 <= col < 8 else None
    
    def handle_click(self, pos):
        """Handle mouse click"""
        square = self.get_square_from_pos(pos)
        if square is None:
            return
        
        row, col = square
        piece = self.board.get_piece_at(square)
        
        # If a piece is selected and we click on a valid move
        if self.selected_square and square in self.valid_moves:
            # Make the move
            if self.board.make_move(self.selected_square, square):
                self.selected_square = None
                self.valid_moves = []
            return
        
        # If we click on a piece of the current player
        if piece and piece.color == self.board.current_player:
            self.selected_square = square
            self.valid_moves = piece.get_valid_moves(self.board)
        else:
            self.selected_square = None
            self.valid_moves = []
    
    def draw_game_status(self):
        """Draw game status information"""
        font = pygame.font.Font(None, 36)
        
        if self.board.game_over:
            text = f"Game Over! {self.board.winner.title()} wins!"
            color = (255, 0, 0)
        else:
            text = f"Current Player: {self.board.current_player.title()}"
            color = (0, 0, 0)
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, 30))
        self.screen.blit(text_surface, text_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.board.game_over:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset game
                        self.board = ChessBoard()
                        self.selected_square = None
                        self.valid_moves = []
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_game_status()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()