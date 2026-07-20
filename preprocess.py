import os
import pickle
from music21 import converter, instrument, note, chord

# Folder containing MIDI files
MIDI_FOLDER = "midi_data"

# Store all notes/chords
notes = []

print("=" * 50)
print("🎵 Music Generation AI - MIDI Preprocessing")
print("=" * 50)

# Read all MIDI files
for file in os.listdir(MIDI_FOLDER):

    if file.endswith(".mid"):

        path = os.path.join(MIDI_FOLDER, file)

        print(f"Reading: {file}")

        midi = converter.parse(path)

        try:
            parts = instrument.partitionByInstrument(midi)

            if parts:
                notes_to_parse = parts.parts[0].recurse()
            else:
                notes_to_parse = midi.flat.notes

        except Exception:
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:

            if isinstance(element, note.Note):
                notes.append(str(element.pitch))

            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

print("\n" + "=" * 50)
print(f"✅ Total Notes/Chords Collected : {len(notes)}")

# Save extracted notes
with open("notes.pkl", "wb") as f:
    pickle.dump(notes, f)

print("✅ notes.pkl saved successfully.")
print("=" * 50)