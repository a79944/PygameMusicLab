# Python Music Lab

**Python Music Lab** is a music sequencer inspired by chrome's music lab, made with python using `pygame`. Users can create songs by activating cells that represent notes in a grid. The tool allows saving/loading patterns, picking the start location of the playback and adjusting tempo.

---

## ✨ Features

* 88-key piano grid with 64 time steps
* Playable in real-time with tempo control
* Instrument selection with various MIDI sounds
* Save/load functionality with up to 3 slots
* Optional playback starting point ("Start From")
* Visual scrollbars and colored note grid

---

## 🎧 How It Works

* Each **row** represents a MIDI note (from A0 to C8)
* Each **column** represents a time step
* When "Play" is pressed (or SPACE), the grid is scanned column-by-column
* Active notes trigger `pygame.midi` to play using selected instrument
* User can scroll both horizontally and vertically
* Tempo is adjustable between 50 BPM and 350 BPM via slider
* Notes are colored based on their pitch (e.g., all Cs have the same tone..etc)

---

## 📂 File Structure

### `main.py`

* Main game loop
* Handles user interaction, drawing, and playback logic

### `config.py`

* Constants for screen size, grid dimensions, colors, and note names

### `grid.py`

* Grid logic: toggling notes, drawing cells, assigning colors and sharps

### `note.py`

* Simple wrapper class to convert note names to MIDI numbers

### `sound_manager.py`

* Manages instrument selection and playback using `pygame.midi`
* Converts note positions to MIDI values
* Plays/Stops MIDI notes

### `save_manager.py`

* Handles saving/loading compositions to/from `.json` files
* Displays a UI menu overlay for save/load slots
* Manages user slot interaction and persistent storage

---

## 🎤 Instruments

Available instruments include:

* Piano
* Church Organ
* Acoustic Guitar
* Violin
* String Ensemble
* Trumpet
* Saxophone
* Flute
* Chiptune (Square Lead)
* Sitar

---

## ⚒️ Requirements

* Python 3.8+
* pygame
* pygame.midi

Install dependencies:

```bash
pip install pygame
```

---

## ▶️ Controls

| Action            | Key/Button              |
| ----------------- | ----------------------- |
| Play/Stop         | Spacebar / "Play"       |
| Save / Load       | HUD Buttons             |
| Clear Grid        | "Clear" Button / R key  |
| Change Instrument | "Instrument" Button     |
| Set Start Column  | "Start From" Button     |
| Scroll Grid       | Arrow Keys / MouseWheel |
| Adjust Tempo      | Slider in HUD           |

Note: After selecting the start column button the user has to choose a column by clicking on a random cell in that column. Furthermore, the scroll bars are draggable.

---

## 💾 Saves

Save files are stored as JSON under the `/saves/` directory in  folder where the executable or main is ran.
Each slot (`slot1.json`, `slot2.json`, `slot3.json`) includes:

* Active cell grid
* Tempo
* Starting column (optional)

---


## 🚀 Future Improvements

* Add support for audio export (WAV)
* Customizable looping of chosen sections
* Add percussion grid
* Allow custom instrument uploads

---

## ✍️ Author

Made by Me and ChatGPT :smiley:

---

## 🎉 License

MIT License. Use freely for personal or educational purposes.
