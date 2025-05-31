import pygame.midi
from note import Note

NOTE_NAMES = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']

def name_to_midi(note_name: str) -> int:
    name = note_name[:-1].lower()
    octave = int(note_name[-1])
    base_index = NOTE_NAMES.index(name)
    return 12 * (octave + 1) + base_index

class SoundManager:
    def __init__(self):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)
        self.instrument_index = 0
        self.instrument_choices = [
            (0, "Piano"),
            (19, "Church Organ"),
            (24, "Acoustic Guitar"),
            (40, "Violin"),
            (48, "String Ensemble"),
            (56, "Trumpet"),
            (64, "Soprano Sax"),
            (73, "Flute"),
            (80, "Square Lead"),
            (104, "Sitar")
        ]
        self.set_instrument_by_index(self.instrument_index)

        self.note_names = []
        for octave in range(0, 9):
            for name in NOTE_NAMES:
                full_name = f"{name}{octave}"
                self.note_names.append(full_name)
                if full_name == "c8":
                    break
            if "c8" in self.note_names:
                break

        self.notes = [Note(name_to_midi(n)) for n in self.note_names]

    def play_notes_at_column(self, column_cells):
        notes_on = []
        for row, is_active in enumerate(column_cells):
            if is_active and 0 <= row < len(self.notes):
                midi_num = self.notes[row].midi_number
                self.player.note_on(midi_num, 127)
                notes_on.append(midi_num)
        return notes_on

    def stop_notes(self, notes):
        for midi_num in notes:
            self.player.note_off(midi_num, 127)


    def play_single_note(self, note_index):
        if 0 <= note_index < len(self.notes):
            midi_num = self.notes[note_index].midi_number
            self.player.note_on(midi_num, 127)
            pygame.time.wait(200)

    def set_instrument_by_index(self, index):
        midi_num, name = self.instrument_choices[index]
        self.instrument_index = index
        self.instrument = midi_num
        self.instrument_name = name
        self.player.set_instrument(midi_num)

    def next_instrument(self):
        self.instrument_index = (self.instrument_index + 1) % len(self.instrument_choices)
        self.set_instrument_by_index(self.instrument_index)