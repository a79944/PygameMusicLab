VISIBLE_ROWS = 24
VISIBLE_COLS = 16

TOTAL_ROWS = 88
TOTAL_COLS = 64

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 720
HUD_HEIGHT = 80
GRID_HEIGHT = SCREEN_HEIGHT - HUD_HEIGHT

CELL_WIDTH = SCREEN_WIDTH // VISIBLE_COLS
CELL_HEIGHT = SCREEN_HEIGHT // VISIBLE_ROWS

FPS = 60


NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_COLORS = {
    'C':  (255, 100, 100),
    'C#': (180, 80, 80),
    'D':  (255, 150, 100),
    'D#': (180, 110, 80),
    'E':  (255, 255, 100),
    'F':  (100, 255, 100),
    'F#': (80, 180, 80),
    'G':  (100, 255, 255),
    'G#': (80, 180, 180),
    'A':  (100, 100, 255),
    'A#': (80, 80, 180),
    'B':  (200, 100, 255)
}
