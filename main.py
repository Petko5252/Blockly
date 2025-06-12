import pygame
import random
import sys

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 750
GRID_SIZE = 9
CELL_SIZE = 55
GRID_ORIGIN = (50, 100)
FPS = 60
DOCK_Y = GRID_ORIGIN[1] + GRID_SIZE * CELL_SIZE + 40  # Block spawn dock vertical pos

# Colors
BG_COLOR_TOP = (20, 22, 25)
BG_COLOR_BOTTOM = (40, 45, 50)
GRID_BG_COLOR = (25, 30, 35)
GRID_CELL_COLOR = (45, 60, 80)
GRID_CELL_HIGHLIGHT = (120, 180, 255)
BLOCK_COLOR = (0, 160, 240)
BLOCK_COLOR_SHADOW = (0, 100, 160)
TEXT_COLOR = (230, 230, 230)
BUTTON_COLOR = (0, 140, 220)
BUTTON_HOVER_COLOR = (0, 180, 255)

# Fonts
TITLE_FONT = pygame.font.SysFont('Segoe UI', 60, bold=True)
font = pygame.font.SysFont('Segoe UI', 28, bold=True)
small_font = pygame.font.SysFont('Segoe UI', 20)
score_font = pygame.font.SysFont('Segoe UI', 24, bold=True)

# Shapes: List of (x,y) relative positions in the block
BLOCK_SHAPES = [
    [(0, 0)],  # Single
    [(0, 0), (1, 0)],  # Horizontal 2
    [(0, 0), (0, 1)],  # Vertical 2
    [(0, 0), (1, 0), (0, 1)],  # L shape
    [(0, 0), (1, 0), (2, 0)],  # Horizontal 3
    [(0, 0), (0, 1), (0, 2)],  # Vertical 3
]

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blockly - The Puzzle Block Game")
clock = pygame.time.Clock()

def draw_text(surface, text, pos, font_obj=font, center=False):
    text_surface = font_obj.render(text, True, TEXT_COLOR)
    if center:
        rect = text_surface.get_rect(center=pos)
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, pos)

def draw_rounded_rect(surface, rect, color, radius=10):
    """Draw rounded rectangle with shadow effect."""
    shadow_color = (0, 0, 0, 50)
    shadow_surf = pygame.Surface((rect.width + 6, rect.height + 6), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, shadow_color, shadow_surf.get_rect(), border_radius=radius)
    surface.blit(shadow_surf, (rect.x + 3, rect.y + 3))
    pygame.draw.rect(surface, color, rect, border_radius=radius)

class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        draw_text(surface, self.text, self.rect.center, font_obj=font, center=True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.callback()

class Block:
    def __init__(self, shape, color):
        self.shape = shape  # List of (x,y)
        self.color = color
        self.position = (0, 0)  # Top-left pixel pos on screen
        self.grid_pos = None  # Grid coords (row, col) when placed
        self.dragging = False
        self.offset = (0, 0)  # Mouse offset

    def draw(self, surface):
        for (x, y) in self.shape:
            rect = pygame.Rect(
                self.position[0] + x * CELL_SIZE + 5,
                self.position[1] + y * CELL_SIZE + 5,
                CELL_SIZE - 10,
                CELL_SIZE - 10,
            )
            # Draw shadow
            shadow_rect = rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(surface, BLOCK_COLOR_SHADOW, shadow_rect, border_radius=8)

            # Draw block
            pygame.draw.rect(surface, self.color, rect, border_radius=8)

    def get_cells(self):
        if self.grid_pos is None:
            return []
        cells = []
        for (x, y) in self.shape:
            r = self.grid_pos[0] + y
            c = self.grid_pos[1] + x
            cells.append((r, c))
        return cells

class Game:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.blocks = []
        self.selected_block = None
        self.score = 0
        self.spawn_blocks()
        self.game_over = False

    def spawn_blocks(self):
        self.blocks = []
        for i in range(3):
            shape = random.choice(BLOCK_SHAPES)
            block = Block(shape, BLOCK_COLOR)
            # Position blocks at the bottom dock
            block.position = (GRID_ORIGIN[0] + i * (CELL_SIZE * 3 + 20), DOCK_Y)
            self.blocks.append(block)

    def draw_background(self):
        # Gradient background top to bottom
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(BG_COLOR_TOP[0] * (1 - ratio) + BG_COLOR_BOTTOM[0] * ratio)
            g = int(BG_COLOR_TOP[1] * (1 - ratio) + BG_COLOR_BOTTOM[1] * ratio)
            b = int(BG_COLOR_TOP[2] * (1 - ratio) + BG_COLOR_BOTTOM[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_grid(self):
        # Grid background
        rect = pygame.Rect(GRID_ORIGIN[0], GRID_ORIGIN[1], CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE)
        pygame.draw.rect(screen, GRID_BG_COLOR, rect, border_radius=15)

        # Cells
        mouse_pos = pygame.mouse.get_pos()
        highlight_cells = []
        if self.selected_block and self.selected_block.dragging:
            # Calculate grid position under mouse
            gx = (mouse_pos[0] - GRID_ORIGIN[0]) // CELL_SIZE
            gy = (mouse_pos[1] - GRID_ORIGIN[1]) // CELL_SIZE
            if self.can_place(self.selected_block, (gy, gx)):
                highlight_cells = [(gy + y, gx + x) for (x, y) in self.selected_block.shape]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_color = GRID_CELL_COLOR
                rect = pygame.Rect(
                    GRID_ORIGIN[0] + col * CELL_SIZE + 5,
                    GRID_ORIGIN[1] + row * CELL_SIZE + 5,
                    CELL_SIZE - 10,
                    CELL_SIZE - 10,
                )
                if (row, col) in highlight_cells:
                    cell_color = GRID_CELL_HIGHLIGHT
                pygame.draw.rect(screen, cell_color, rect, border_radius=8)

                if self.grid[row][col] is not None:
                    # Draw placed block with shadow
                    shadow_rect = rect.copy()
                    shadow_rect.x += 3
                    shadow_rect.y += 3
                    pygame.draw.rect(screen, BLOCK_COLOR_SHADOW, shadow_rect, border_radius=8)
                    pygame.draw.rect(screen, BLOCK_COLOR, rect, border_radius=8)

    def can_place(self, block, grid_pos):
        for (x, y) in block.shape:
            r = grid_pos[0] + y
            c = grid_pos[1] + x
            if r < 0 or r >= GRID_SIZE or c < 0 or c >= GRID_SIZE:
                return False
            if self.grid[r][c] is not None:
                return False
        return True

    def place_block(self, block, grid_pos):
        if not self.can_place(block, grid_pos):
            return False
        for (x, y) in block.shape:
            r = grid_pos[0] + y
            c = grid_pos[1] + x
            self.grid[r][c] = block.color
        block.grid_pos = grid_pos
        if block in self.blocks:
            self.blocks.remove(block)
        self.clear_lines()
        if len(self.blocks) == 0:
            self.spawn_blocks()
        if not self.any_moves_left():
            self.game_over = True
        return True

    def clear_lines(self):
        full_rows = [r for r in range(GRID_SIZE) if all(self.grid[r][c] is not None for c in range(GRID_SIZE))]
        full_cols = [c for c in range(GRID_SIZE) if all(self.grid[r][c] is not None for r in range(GRID_SIZE))]

        cleared = 0

        for r in full_rows:
            for c in range(GRID_SIZE):
                self.grid[r][c] = None
            cleared += 1

        for c in full_cols:
            for r in range(GRID_SIZE):
                self.grid[r][c] = None
            cleared += 1

        self.score += cleared * 10

    def any_moves_left(self):
        # Check if any block can be placed somewhere on grid
        for block in self.blocks:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.can_place(block, (r, c)):
                        return True
        return False

    def draw_score(self):
        # Score panel background
        panel_rect = pygame.Rect(400, 20, 170, 60)
        pygame.draw.rect(screen, GRID_BG_COLOR, panel_rect, border_radius=12)
        draw_text(screen, f"Score:", (410, 25), font_obj=score_font)
        draw_text(screen, f"{self.score}", (410, 50), font_obj=score_font)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        draw_text(screen, "Game Over!", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40), font_obj=TITLE_FONT, center=True)
        draw_text(screen, f"Final Score: {self.score}", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20), font_obj=font, center=True)
        draw_text(screen, "Press ESC to return to Menu", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), font_obj=small_font, center=True)

    def run(self):
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.game_over:
                        return  # Return to menu

                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    for block in self.blocks:
                        bx, by = block.position
                        width = max(x for x, _ in block.shape) + 1
                        height = max(y for _, y in block.shape) + 1
                        block_rect = pygame.Rect(bx, by, width * CELL_SIZE, height * CELL_SIZE)
                        if block_rect.collidepoint(pos):
                            block.dragging = True
                            self.selected_block = block
                            block.offset = (pos[0] - bx, pos[1] - by)
                            break

                elif event.type == pygame.MOUSEBUTTONUP and not self.game_over:
                    if self.selected_block and self.selected_block.dragging:
                        mx, my = pygame.mouse.get_pos()
                        gx = (mx - GRID_ORIGIN[0]) // CELL_SIZE
                        gy = (my - GRID_ORIGIN[1]) // CELL_SIZE
                        if self.place_block(self.selected_block, (gy, gx)):
                            self.selected_block.position = (0, 0)
                            self.selected_block.grid_pos = (gy, gx)
                        else:
                            # Return to dock
                            idx = self.blocks.index(self.selected_block) if self.selected_block in self.blocks else -1
                            if idx == -1:
                                self.selected_block.position = (-1000, -1000)  # Hide removed block
                            else:
                                self.selected_block.position = (GRID_ORIGIN[0] + idx * (CELL_SIZE * 3 + 20), DOCK_Y)

                        self.selected_block.dragging = False
                        self.selected_block = None

                elif event.type == pygame.MOUSEMOTION and not self.game_over:
                    if self.selected_block and self.selected_block.dragging:
                        mx, my = pygame.mouse.get_pos()
                        ox, oy = self.selected_block.offset
                        self.selected_block.position = (mx - ox, my - oy)

            self.draw_background()
            self.draw_grid()
            self.draw_score()

            for block in self.blocks:
                block.draw(screen)

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()

class MainMenu:
    def __init__(self):
        self.play_button = Button(rect=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60), text="Play", callback=self.start_game)
        self.running = True
        self.start_game_flag = False

    def start_game(self):
        self.start_game_flag = True

    def draw_background(self):
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(BG_COLOR_TOP[0] * (1 - ratio) + BG_COLOR_BOTTOM[0] * ratio)
            g = int(BG_COLOR_TOP[1] * (1 - ratio) + BG_COLOR_BOTTOM[1] * ratio)
            b = int(BG_COLOR_TOP[2] * (1 - ratio) + BG_COLOR_BOTTOM[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def run(self):
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.play_button.handle_event(event)

            self.draw_background()
            # Draw title
            draw_text(screen, "Blockly", (SCREEN_WIDTH // 2, 150), font_obj=TITLE_FONT, center=True)
            draw_text(screen, "Drag blocks to fill the grid rows and columns", (SCREEN_WIDTH // 2, 220), font_obj=small_font, center=True)

            self.play_button.draw(screen)

            pygame.display.flip()

            if self.start_game_flag:
                self.running = False


def main():
    menu = MainMenu()
    menu.run()
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
