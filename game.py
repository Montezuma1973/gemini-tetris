from grid import Grid
from blocks import *
import random
import pygame

class Game:
    """
    Main game logic class.
    Manages the grid, blocks, score, and game state.
    """
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound('Sounds/rotate.ogg')
        self.clear_sound = pygame.mixer.Sound('Sounds/clear.ogg')

    def update_score(self, lines_cleared, move_down_points):
        """Updates the score based on lines cleared and movement."""
        if lines_cleared == 1:
            self.score += 100
            self.clear_sound.play()
        elif lines_cleared == 2:
            self.score += 300
            self.clear_sound.play()
        elif lines_cleared == 3:
            self.score += 500
            self.clear_sound.play()
        elif lines_cleared == 4:
            self.score += 1000 # Tetris!
            self.clear_sound.play()
        self.score += move_down_points

    def get_random_block(self):
        """Returns a random block from the available set. Refills if empty."""
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        """Moves the current block left if possible."""
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        """Moves the current block right if possible."""
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        """Moves the current block down. Locks it if it hits the bottom."""
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        """Locks the current block into the grid and checks for cleared lines."""
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        """Resets the game state to start a new game."""
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False

    def block_fits(self):
        """Checks if the current block fits in its current position (no collisions)."""
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        """Rotates the current block if possible."""
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        """Checks if the current block is entirely within the grid boundaries."""
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, screen):
        """Draws the game elements (grid and current block) on the screen."""
        self.grid.draw(screen)
        self.current_block.draw(screen)
