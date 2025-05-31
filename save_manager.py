import os
import json
import sys
import pygame
from config import *

class SaveManager:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        self.folder = os.path.join(base_path, "saves")
        os.makedirs(self.folder, exist_ok=True)

        self.active = False
        self.mode = None
        self.slot_buttons = []
        self.font = pygame.font.SysFont(None, 24)

    def draw_menu(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.font.render(f"{self.mode.capitalize()} Menu", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - 50, 50))

        self.slot_buttons = []
        for i in range(3):
            y = 120 + i * 70
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, y, 200, 50)
            pygame.draw.rect(screen, (80, 80, 80), rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)

            slot_path = os.path.join(self.folder, f"slot{i + 1}.json")
            label = "Saved" if os.path.exists(slot_path) else "Empty"
            text = self.font.render(f"Slot {i + 1}: {label}", True, (255, 255, 255))
            screen.blit(text, (rect.x + 20, rect.y + 15))
            self.slot_buttons.append((rect, i + 1))

    def handle_click(self, pos, grid, tempo, start_col_marker):
        for rect, slot_num in self.slot_buttons:
            if rect.collidepoint(pos):
                if self.mode == "save":
                    self.save_to_slot(slot_num, grid, tempo, start_col_marker)
                elif self.mode == "load":
                    self.load_from_slot(slot_num, grid)
                self.active = False
                return

    def save_to_slot(self, slot_num, grid, tempo, start_col_marker):
        data = {
            "cells": grid.cells,
            "tempo": tempo,
            "start_col_marker": start_col_marker
        }
        with open(os.path.join(self.folder, f"slot{slot_num}.json"), "w") as f:
            json.dump(data, f)

    def load_from_slot(self, slot_num, grid):
        path = os.path.join(self.folder, f"slot{slot_num}.json")
        if os.path.exists(path):
            #(path)
            with open(path, "r") as f:
                data = json.load(f)
            grid.cells = data.get("cells", grid.cells)
            global tempo, play_delay, start_col_marker
            tempo = data.get("tempo", 150)
            play_delay = int(60000 / tempo)
            start_col_marker = data.get("start_col_marker", None)
