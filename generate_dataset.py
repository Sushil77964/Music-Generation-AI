from pathlib import Path
import random

from music21 import chord, instrument, note, stream, tempo


OUTPUT_DIR = Path("midi_data")
OUTPUT_DIR.mkdir(exist_ok=True)

SCALES = {
    "C_major": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
    "A_minor": ["A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4"],
    "G_major": ["G3", "A3", "B3", "C4", "D4", "E4", "F#4", "G4"],
}

CHORDS = [
    ["C4", "E4", "G4"],
    ["F4", "A4", "C5"],
    ["G4", "B4", "D5"],
    ["A3", "C4", "E4"],
]


def create_melody(file_number: int) -> None:
    music_stream = stream.Stream()
    music_stream.append(instrument.Piano())
    music_stream.append(tempo.MetronomeMark(number=random.randint(80, 130)))

    scale_name = random.choice(list(SCALES.keys()))
    scale_notes = SCALES[scale_name]

    for _ in range(random.randint(40, 70)):
        if random.random() < 0.2:
            selected_chord = random.choice(CHORDS)
            new_chord = chord.Chord(selected_chord)
            new_chord.quarterLength = random.choice([0.5, 1.0, 2.0])
            music_stream.append(new_chord)
        else:
            selected_note = random.choice(scale_notes)
            new_note = note.Note(selected_note)
            new_note.quarterLength = random.choice([0.25, 0.5, 1.0, 1.5])
            music_stream.append(new_note)

    output_path = OUTPUT_DIR / f"practice_melody_{file_number:02d}.mid"
    music_stream.write("midi", fp=str(output_path))
    print(f"Created: {output_path}")


def main() -> None:
    total_files = 30

    for index in range(1, total_files + 1):
        create_melody(index)

    print(f"\nDone! {total_files} MIDI files created in '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    main()