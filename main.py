import pygame
import sys
from config import *
from grid import Grid
from sound_manager import SoundManager
from save_manager import SaveManager

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Music Lab")
clock = pygame.time.Clock()
save_manager = SaveManager()

grid = Grid()
sound_manager = SoundManager()


start_row = (TOTAL_ROWS - VISIBLE_ROWS) // 2
start_col = 0


scroll_dragging_vert = False
scroll_dragging_horiz = False
scroll_offset_y = 0
scroll_offset_x = 0

slider_x = 840
slider_width = 200
slider_dragging = False
tempo = 150



play_col = 0
is_playing = False
play_delay = int(60000 / tempo)
last_play_time = pygame.time.get_ticks()

set_start_mode = False
start_col_marker = None



def draw_scrollbars(surface, start_row, start_col):

    bar_height = SCREEN_HEIGHT * (VISIBLE_ROWS / TOTAL_ROWS)
    bar_y = SCREEN_HEIGHT * (start_row / TOTAL_ROWS)
    pygame.draw.rect(surface, (100, 100, 100), (SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT))
    pygame.draw.rect(surface, (200, 200, 200), (SCREEN_WIDTH - 10, bar_y, 10, bar_height))


    bar_width = SCREEN_WIDTH * (VISIBLE_COLS / TOTAL_COLS)
    bar_x = SCREEN_WIDTH * (start_col / TOTAL_COLS)
    pygame.draw.rect(surface, (100, 100, 100), (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10))
    pygame.draw.rect(surface, (200, 200, 200), (bar_x, SCREEN_HEIGHT - 10, bar_width, 10))

while True:
    screen.fill((30, 30, 30))
    grid.draw(screen, start_row, start_col, VISIBLE_ROWS, VISIBLE_COLS)
    hud_rect = pygame.Rect(0, SCREEN_HEIGHT - HUD_HEIGHT, SCREEN_WIDTH, HUD_HEIGHT)
    pygame.draw.rect(screen, (0, 0, 0), hud_rect)
    font = pygame.font.SysFont(None, 24)
    buttons = [("Play", 20), ("Clear", 150), ("Save", 280), ("Load", 410), ("Start From", 540), ("Instrument", 680)]

    for label, x in buttons:
        btn_text = "Stop" if label == "Play" and is_playing else label
        if label == "Instrument":
            btn_text = f"{sound_manager.instrument_name}"
            text = font.render(btn_text, True, (255, 255, 255))
            rect = pygame.Rect(x, SCREEN_HEIGHT - HUD_HEIGHT + 20, text.get_width() + 20, 40)
        else:
            text = font.render(btn_text, True, (255, 255, 255))
            rect = pygame.Rect(x, SCREEN_HEIGHT - HUD_HEIGHT + 20, 100, 40)

        pygame.draw.rect(screen, (60, 60, 60), rect)
        pygame.draw.rect(screen, (180, 180, 180), rect, 2)
        screen.blit(text, (rect.x + 10, rect.y + 10))

        pygame.draw.rect(screen, (80, 80, 80), (slider_x, SCREEN_HEIGHT - HUD_HEIGHT + 30, slider_width, 10))
        slider_pos = int(slider_x + (tempo - 50) / 300 * slider_width)
        pygame.draw.circle(screen, (200, 200, 0), (slider_pos, SCREEN_HEIGHT - HUD_HEIGHT + 35), 8)
        text = font.render("Tempo", True, (255, 255, 255))
        screen.blit(text, (slider_x, SCREEN_HEIGHT - HUD_HEIGHT + 10))

    draw_scrollbars(screen, start_row, start_col)
    if save_manager.active:
        save_manager.draw_menu(screen)

    for event in pygame.event.get():

        if save_manager.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                save_manager.handle_click(pygame.mouse.get_pos(), grid, tempo, start_col_marker)
            continue
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()

            horiz_bar_width = SCREEN_WIDTH * (VISIBLE_COLS / TOTAL_COLS)
            horiz_bar_x = SCREEN_WIDTH * (start_col / TOTAL_COLS)
            if SCREEN_HEIGHT - 10 <= y <= SCREEN_HEIGHT and horiz_bar_x <= x <= horiz_bar_x + horiz_bar_width:
                scroll_dragging_horiz = True
                scroll_offset_x = x - horiz_bar_x
                continue

            if y >= SCREEN_HEIGHT - HUD_HEIGHT:
                for label, x_btn in buttons:
                    rect = pygame.Rect(x_btn, SCREEN_HEIGHT - HUD_HEIGHT + 20, 100, 40)
                    if rect.collidepoint(x, y):
                        if label == "Play":
                            if is_playing:
                                is_playing = False
                                if hasattr(sound_manager, "previous_notes"):
                                    sound_manager.stop_notes(sound_manager.previous_notes)
                                    sound_manager.previous_notes = []
                            else:
                                is_playing = True
                                play_col = start_col_marker if start_col_marker is not None else 0
                                last_play_time = pygame.time.get_ticks()
                        elif label == "Clear":
                            grid.clear_all()
                        elif label == "Save":
                            save_manager.active = True
                            save_manager.mode = "save"
                        elif label == "Load":
                            save_manager.active = True
                            save_manager.mode = "load"
                        elif label == "Start From":
                            set_start_mode = not set_start_mode
                        elif label == "Instrument":
                            sound_manager.next_instrument()

                        break
                if slider_x <= x <= slider_x + slider_width and SCREEN_HEIGHT - HUD_HEIGHT + 20 <= y <= SCREEN_HEIGHT:
                    slider_dragging = True
                    relative = x - slider_x
                    tempo = int(50 + (relative / slider_width) * 300)
                    play_delay = int(60000 / tempo)
                continue

            vert_bar_height = SCREEN_HEIGHT * (VISIBLE_ROWS / TOTAL_ROWS)
            vert_bar_y = SCREEN_HEIGHT * (start_row / TOTAL_ROWS)
            if SCREEN_WIDTH - 10 <= x <= SCREEN_WIDTH and vert_bar_y <= y <= vert_bar_y + vert_bar_height:
                scroll_dragging_vert = True
                scroll_offset_y = y - vert_bar_y
                continue

            if x >= SCREEN_WIDTH - 10 or y >= SCREEN_HEIGHT - 10:
                continue

            if set_start_mode:
                col = x // CELL_WIDTH + start_col
                if 0 <= col < TOTAL_COLS:
                    if start_col_marker == col:
                        start_col_marker = None
                    else:
                        start_col_marker = col
                set_start_mode = False
                continue

            col = x // CELL_WIDTH + start_col
            row = TOTAL_ROWS - 1 - (y // CELL_HEIGHT + start_row)
            if 0 <= row < TOTAL_ROWS and 0 <= col < TOTAL_COLS:
                grid.toggle_cell(row, col)

                if grid.cells[row][col]:
                    note_index = row
                    sound_manager.play_single_note(note_index)
                    sound_manager.previous_notes = [sound_manager.notes[note_index].midi_number]
                    if hasattr(sound_manager, "previous_notes"):
                        sound_manager.stop_notes(sound_manager.previous_notes)



        elif event.type == pygame.MOUSEBUTTONUP:
            scroll_dragging_vert = False
            scroll_dragging_horiz = False
            slider_dragging = False


        elif event.type == pygame.MOUSEMOTION:
            if scroll_dragging_vert:
                y = pygame.mouse.get_pos()[1]
                new_y = y - scroll_offset_y
                new_start_row = int((new_y / SCREEN_HEIGHT) * TOTAL_ROWS)
                start_row = max(0, min(new_start_row, TOTAL_ROWS - VISIBLE_ROWS))
            if scroll_dragging_horiz:
                x = pygame.mouse.get_pos()[0]
                new_x = x - scroll_offset_x
                new_start_col = int((new_x / SCREEN_WIDTH) * TOTAL_COLS)
                start_col = max(0, min(new_start_col, TOTAL_COLS - VISIBLE_COLS))
            if slider_dragging:
                x = pygame.mouse.get_pos()[0]
                relative = max(0, min(x - slider_x, slider_width))
                tempo = int(50 + (relative / slider_width) * 300)
                play_delay = int(60000 / tempo)

        elif event.type == pygame.MOUSEWHEEL:
            start_row -= event.y
            start_row = max(0, min(start_row, TOTAL_ROWS - VISIBLE_ROWS))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if is_playing:
                    is_playing = False
                    if hasattr(sound_manager, "previous_notes"):
                        sound_manager.stop_notes(sound_manager.previous_notes)
                        sound_manager.previous_notes = []
                else:
                    is_playing = True
                    play_col = start_col_marker if start_col_marker is not None else 0
                    last_play_time = pygame.time.get_ticks()

            elif event.key == pygame.K_UP and start_row > 0:
                start_row -= 1
            elif event.key == pygame.K_DOWN and start_row + VISIBLE_ROWS < TOTAL_ROWS:
                start_row += 1
            elif event.key == pygame.K_LEFT and start_col > 0:
                start_col -= 1
            elif event.key == pygame.K_RIGHT and start_col + VISIBLE_COLS < TOTAL_COLS:
                start_col += 1
            elif event.key == pygame.K_r:
                grid.clear_all()

    if is_playing:
        now = pygame.time.get_ticks()
        if now - last_play_time >= play_delay:
            if hasattr(sound_manager, "previous_notes"):
                sound_manager.stop_notes(sound_manager.previous_notes)
            column_cells = [grid.cells[row][play_col] for row in range(TOTAL_ROWS)]

            next_col = play_col + 1

            notes_remaining = any(
                any(grid.cells[row][col] for row in range(TOTAL_ROWS))
                for col in range(next_col-2, TOTAL_COLS)
            )

            if not notes_remaining:
                is_playing = False
                if hasattr(sound_manager, "previous_notes"):
                    sound_manager.stop_notes(sound_manager.previous_notes)
                    sound_manager.previous_notes = []
                continue

            active_notes = sound_manager.play_notes_at_column(column_cells)


            sound_manager.previous_notes = active_notes

            if next_col >= TOTAL_COLS:
                is_playing = False
                if hasattr(sound_manager, "previous_notes"):
                    sound_manager.stop_notes(sound_manager.previous_notes)
                    sound_manager.previous_notes = []
            else:
                gap = next_col - play_col
                play_col = next_col
                last_play_time = now
        if start_col <= play_col < start_col + VISIBLE_COLS:
            bar_x = (play_col - 1 - start_col) * CELL_WIDTH + CELL_WIDTH // 4
            bar_rect = pygame.Rect(bar_x, 0, CELL_WIDTH // 2, SCREEN_HEIGHT - HUD_HEIGHT)
            pygame.draw.rect(screen, (0, 255, 0), bar_rect)
    if start_col_marker is not None and start_col <= start_col_marker < start_col + VISIBLE_COLS:
        marker_x = (start_col_marker - start_col) * CELL_WIDTH
        pygame.draw.rect(screen, (255, 0, 0), (marker_x, 0, CELL_WIDTH, SCREEN_HEIGHT - HUD_HEIGHT), 3)
    pygame.display.flip()
    clock.tick(FPS)
