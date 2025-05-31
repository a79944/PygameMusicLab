import pygame
from config import TOTAL_ROWS, TOTAL_COLS, CELL_WIDTH, CELL_HEIGHT, NOTE_NAMES, NOTE_COLORS


class Grid:
    def __init__(self):
        self.cells = [[False for _ in range(TOTAL_COLS)] for _ in range(TOTAL_ROWS)]

    def toggle_cell(self, row, col):
        self.cells[row][col] = not self.cells[row][col]

    def draw(self, surface, start_row, start_col, visible_rows, visible_cols):
        font = pygame.font.SysFont(None, 16)

        for row in range(visible_rows):
            if (start_row + row) % 12 == 0:
                pygame.draw.line(surface, (255, 255, 255), (0, row * CELL_HEIGHT),
                                 (visible_cols * CELL_WIDTH, row * CELL_HEIGHT), 2)
            for col in range(visible_cols):
                grid_row = TOTAL_ROWS - 1 - (start_row + row)
                grid_col = start_col + col
                if grid_row >= TOTAL_ROWS or grid_col >= TOTAL_COLS:
                    continue
                rect = pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                note_name = self.get_note_name_for_row(grid_row)
                base_color = NOTE_COLORS[note_name]

                if self.cells[grid_row][grid_col]:
                    color = base_color
                else:
                    color = tuple(c // 3 for c in base_color)

                pygame.draw.rect(surface, color, rect)

                label_text = font.render(note_name.upper(), True, (255, 255, 255))
                text_rect = label_text.get_rect()
                text_x = rect.right - text_rect.width - 2
                text_y = rect.y + 2
                surface.blit(label_text, (text_x, text_y))

                pygame.draw.rect(surface, (200, 200, 200), rect, 1)

    def get_note_name_for_row(self, row_index):
        midi_number = self.get_midi_number_for_row(row_index)
        note_index = midi_number % 12
        return NOTE_NAMES[note_index]

    def get_midi_number_for_row(self, row_index):
        return 24 + row_index

    def clear_all(self):
        for row in range(TOTAL_ROWS):
            for col in range(TOTAL_COLS):
                self.cells[row][col] = False
