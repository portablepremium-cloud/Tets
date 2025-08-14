# Chess Game in Python

A complete chess game implementation in Python with two versions: a graphical interface using Pygame and a terminal-based version.

## Features

- **Complete Chess Rules**: All standard chess pieces with proper movement validation
- **Two Interface Options**: Graphical (Pygame) and Terminal-based
- **Move Validation**: Prevents illegal moves and shows valid move hints
- **Game State Management**: Tracks current player, game over conditions, and winner
- **Pawn Promotion**: Automatic promotion to queen when pawn reaches the opposite end
- **Visual Feedback**: Highlights selected pieces and valid moves (graphical version)

## Installation

### Option 1: Terminal Version (No Dependencies)
The terminal version requires no additional dependencies and works with any Python installation.

```bash
python3 chess_terminal.py
```

### Option 2: Graphical Version (Requires Pygame)
1. **Install Python** (version 3.7 or higher)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install pygame directly:
   ```bash
   pip install pygame
   ```

3. **Run the graphical version**:
   ```bash
   python chess_game.py
   ```

## How to Play

### Terminal Version
1. **Run the game**:
   ```bash
   python3 chess_terminal.py
   ```

2. **Game Controls**:
   - **Move Format**: Enter moves as `e2e4` (from square to square)
   - **Commands**: 
     - `quit` - Exit the game
     - `reset` - Start a new game
     - `help` - Show instructions

3. **Gameplay**:
   - White pieces start first
   - Enter moves using chess notation (e.g., `e2e4`, `g1f3`)
   - The game validates moves and prevents illegal ones
   - Pawns automatically promote to queens when reaching the opposite end

### Graphical Version
1. **Game Controls**:
   - **Mouse Click**: Select pieces and make moves
   - **R Key**: Reset the game
   - **Close Window**: Quit the game

2. **Gameplay**:
   - White pieces start first
   - Click on a piece to select it (highlighted in yellow)
   - Valid moves are shown in green
   - Click on a green square to make a move
   - The game automatically switches between players

## Game Rules

### Piece Movements

- **Pawn**: Moves forward one square (or two from starting position), captures diagonally
- **Rook**: Moves horizontally and vertically any number of squares
- **Knight**: Moves in L-shape (2 squares in one direction, 1 square perpendicular)
- **Bishop**: Moves diagonally any number of squares
- **Queen**: Combines rook and bishop movements
- **King**: Moves one square in any direction

### Game End Conditions

- **Checkmate**: When a player has no valid moves and their king is in check
- **Stalemate**: When a player has no valid moves but their king is not in check

## Code Structure

- `ChessPiece`: Represents individual chess pieces with movement logic
- `ChessBoard`: Manages the game board state and move validation
- `ChessGame`: Handles the interface and user interaction

## Files

- `chess_terminal.py` - Terminal-based chess game (no dependencies)
- `chess_game.py` - Graphical chess game using Pygame
- `requirements.txt` - Python dependencies for graphical version

## Future Enhancements

- Add proper chess piece images
- Implement castling
- Add en passant capture
- Include move history
- Add save/load game functionality
- Implement AI opponent
- Add sound effects
- Add check detection and highlighting

## Requirements

### Terminal Version
- Python 3.7+ (no additional dependencies)

### Graphical Version
- Python 3.7+
- Pygame 2.5.2

## License

This project is open source and available under the MIT License.