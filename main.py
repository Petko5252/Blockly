from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
import random

# Set window size for desktop testing (optional)
Window.size = (360, 640)

# Load the KV file if it exists
import os
if os.path.exists('game.kv'):
    Builder.load_file('game.kv')
else:
    print("Warning: 'game.kv' not found. Please ensure the KV file is present.")

# Constants
GRID_ROWS = 8
GRID_COLS = 8
BLOCK_SIZE = dp(40)  # Size of one block (button)

# Define colors for blocks (Kivy RGBA)
COLORS = [
    [0.9, 0.2, 0.2, 1],  # Red
    [0.2, 0.8, 0.2, 1],  # Green
    [0.2, 0.4, 0.8, 1],  # Blue
    [0.9, 0.7, 0.2, 1],  # Yellow
    [0.7, 0.2, 0.7, 1],  # Purple
]


class Block(Button):
    """A block in the game grid."""
    color_index = NumericProperty(0)

    def __init__(self, row, col, color_index, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.color_index = color_index
        self.background_normal = ''
        self.background_color = COLORS[self.color_index]
        self.font_size = dp(0)  # hide text
        self.border = (0, 0, 0, 0)
        self.size_hint = (None, None)
        self.size = (BLOCK_SIZE, BLOCK_SIZE)

    def blast(self):
        """Hide this block by making it transparent or removing."""
        self.background_color = [0, 0, 0, 0]
        self.color_index = -1
        self.disabled = True


class GameGrid(GridLayout):
    """Grid layout that holds blocks."""

    def __init__(self, game_screen, **kwargs):
        super().__init__(**kwargs)
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.game_screen = game_screen
        self.blocks = []
        self.populate_grid()

        # Set fixed size and remove size_hint to control centering and size
        self.size_hint = (None, None)
        self.size = (BLOCK_SIZE * GRID_COLS, BLOCK_SIZE * GRID_ROWS)

    def populate_grid(self):
        """Create blocks with random colors."""
        self.blocks.clear()
        self.clear_widgets()
        for row in range(self.rows):
            row_blocks = []
            for col in range(self.cols):
                color_idx = random.randint(0, len(COLORS) - 1)
                block = Block(row, col, color_idx)
                block.bind(on_release=self.on_block_press)
                self.add_widget(block)
                row_blocks.append(block)
            self.blocks.append(row_blocks)

    def on_block_press(self, block):
        """Handle block press event."""
        if block.color_index == -1:
            # Already blasted
            return
        cluster = self.find_cluster(block.row, block.col, block.color_index)
        if len(cluster) <= 1:
            # Only blast clusters >= 2, else no blast
            return
        self.blast_cluster(cluster)
        self.drop_blocks()
        self.game_screen.update_score(len(cluster))

    def find_cluster(self, row, col, color_index):
        """Find all connected blocks of the same color."""
        visited = set()
        to_visit = [(row, col)]
        cluster = []

        while to_visit:
            r, c = to_visit.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            block = self.blocks[r][c]
            if block.color_index == color_index:
                cluster.append(block)
                # Check neighbors
                neighbors = self.get_neighbors(r, c)
                for nr, nc in neighbors:
                    if (nr, nc) not in visited:
                        to_visit.append((nr, nc))
        return cluster

    def get_neighbors(self, r, c):
        """Return valid neighbors (up, down, left, right)."""
        neighbors = []
        if r > 0:
            neighbors.append((r - 1, c))
        if r < self.rows - 1:
            neighbors.append((r + 1, c))
        if c > 0:
            neighbors.append((r, c - 1))
        if c < self.cols - 1:
            neighbors.append((r, c + 1))
        return neighbors

    def blast_cluster(self, cluster):
        """Blast all blocks in cluster."""
        for block in cluster:
            block.blast()

    def drop_blocks(self):
        """Drop blocks down in columns and fill empty places from top."""
        for col in range(self.cols):
            # Extract blocks column by column
            column_blocks = [self.blocks[row][col] for row in range(self.rows)]
            # Filter out blasted blocks
            alive_blocks = [b for b in column_blocks if b.color_index != -1]
            num_blasted = self.rows - len(alive_blocks)
            # Move alive blocks down by filling from bottom
            for i in range(len(alive_blocks)):
                block = alive_blocks[-1 - i]
                dest_row = self.rows - 1 - i
                if block.row != dest_row:
                    self.move_block(block, dest_row, col)
            # Replace blasted blocks on top with new random blocks
            for i in range(num_blasted):
                new_row = i
                new_color_idx = random.randint(0, len(COLORS) - 1)
                block = self.blocks[new_row][col]
                block.color_index = new_color_idx
                block.background_color = COLORS[new_color_idx]
                block.disabled = False

    def move_block(self, block, new_row, new_col):
        """Move a block logically (without changing widget position)."""
        # Swap block objects in self.blocks grid
        dest_block = self.blocks[new_row][new_col]

        # Swap properties instead of swapping widgets to keep same buttons
        dest_block.color_index = block.color_index
        dest_block.background_color = COLORS[block.color_index]
        dest_block.disabled = block.disabled

        # Blast the original block (because its info moved)
        block.color_index = -1
        block.background_color = [0, 0, 0, 0]
        block.disabled = True

    def reset_grid(self):
        self.populate_grid()


class HomeScreen(Screen):
    pass


class GameScreen(Screen):
    score = NumericProperty(0)

    def on_kv_post(self, base_widget):
        # This is called after kv ids are ready; add the grid to grid_placeholder
        self.grid = GameGrid(self)
        self.ids.grid_placeholder.add_widget(self.grid)

    def update_score(self, points):
        self.score += points * (points - 1)
        self.ids.score_label.text = f"Score: {self.score}"

    def reset_game(self, *args):
        self.score = 0
        self.ids.score_label.text = "Score: 0"
        self.grid.reset_grid()


class BlockBlastApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GameScreen(name='game'))
        sm.current = 'home'  # Set default screen
        return sm


if __name__ == '__main__':
    app = BlockBlastApp()
    app.icon = 'Blockly.png'  # Link the app window icon here
    app.run()
