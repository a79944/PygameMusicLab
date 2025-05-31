import pygame.midi

from config import NOTE_NAMES


class Note:
    def __init__(self, midi_number: int):
        self.midi_number = midi_number

    def name_to_midi(self, note_name: str) -> int:
        name = note_name[:-1].lower()
        octave = int(note_name[-1])
        base_index = NOTE_NAMES.index(name)
        return 12 * (octave + 1) + base_index


