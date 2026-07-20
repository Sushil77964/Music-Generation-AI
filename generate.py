from transformers import pipeline

print("=" * 50)
print("Loading Meta MusicGen Model...")
print("=" * 50)

generator = pipeline(
    "text-to-audio",
    model="facebook/musicgen-small"
)

prompt = input("Enter music prompt: ")

print("\nGenerating music...\n")

music = generator(
    prompt,
    forward_params={
        "do_sample": True,
        "max_new_tokens": 256
    }
)

audio = music["audio"]

sampling_rate = music["sampling_rate"]

import soundfile as sf

sf.write(
    "generated_music.wav",
    audio,
    sampling_rate
)

print("\nMusic Generated Successfully!")
print("Saved as generated_music.wav")