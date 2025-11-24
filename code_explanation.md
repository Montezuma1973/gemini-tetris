# Tetris Code Explanation

This document explains the structure and logic of the Python Tetris game.

## Project Structure

The project is divided into several files, each handling a specific part of the game:

*   **`main.py`**: The entry point of the game. It sets up the window, handles user input, and runs the game loop.
*   **`game.py`**: Contains the `Game` class, which manages the overall game state (score, current block, next block, game over status).
*   **`grid.py`**: Contains the `Grid` class, representing the game board. It handles storing locked blocks and checking for full lines.
*   **`blocks.py`**: Defines the `Block` base class and the 7 specific tetromino shapes (I, J, L, O, S, T, Z).
*   **`colors.py`**: Defines the color palette used for the blocks and UI.

## Core Concepts

### The Grid (`grid.py`)
The game board is a 20x10 grid represented by a 2D list (list of lists).
*   `0` represents an empty cell.
*   Numbers `1-7` represent the colors of the locked blocks.
*   **Coordinate System**: Row 0 is the top, Row 19 is the bottom. Column 0 is left, Column 9 is right.

### The Blocks (`blocks.py`)
Each tetromino is a subclass of the `Block` class.
*   **`cells`**: A dictionary storing the relative positions of the block's cells for each rotation state (0, 1, 2, 3).
*   **`move(rows, columns)`**: Changes the block's offset to move it around the grid.
*   **`rotate()`**: Cycles through the rotation states.

### The Game Logic (`game.py`)
The `Game` class ties everything together.
*   **`move_down()`**: Moves the current block down. If it collides, it calls `lock_block()`.
*   **`lock_block()`**:
    1.  Writes the current block's ID into the `Grid`.
    2.  Checks for full rows and clears them (`grid.clear_full_rows()`).
    3.  Updates the score.
    4.  Spawns a new block.
    5.  Checks for Game Over (if the new block doesn't fit).

### The Game Loop (`main.py`)
This is the "heart" of the game, running 60 times per second.
1.  **Event Handling**: Checks for keyboard inputs (Left, Right, Down, Up/Rotate) and the "QUIT" event.
2.  **Game Updates**: Moves the block down automatically every 200ms (controlled by a custom event `GAME_UPDATE`).
3.  **Drawing**: Clears the screen, draws the score, the grid, and the current block, then updates the display.

## Key Functions

*   `grid.clear_full_rows()`: Scans from bottom to top. If a row is full, it clears it and moves all rows above it down.
*   `game.block_fits()`: Checks if the current block's position overlaps with any existing blocks in the grid.
*   `game.rotate()`: Rotates the block. If the new rotation hits a wall or another block, it immediately undoes the rotation (`undo_rotation()`).
