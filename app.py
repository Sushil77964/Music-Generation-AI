from pathlib import Path

import soundfile as sf
import streamlit as st
from transformers import pipeline


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "generated_music.wav"


@st.cache_resource
def load_music_model():
    return pipeline(
        task="text-to-audio",
        model="facebook/musicgen-small"
    )


st.set_page_config(
    page_title="Music Generation AI",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Music Generation AI")
st.write(
    "Describe the type of music you want, and AI will generate it for you."
)

prompt = st.text_area(
    "Enter your music prompt",
    placeholder="Example: A relaxing piano melody with soft rain sounds",
    height=120
)

duration_tokens = st.slider(
    "Music length",
    min_value=128,
    max_value=512,
    value=256,
    step=64
)

if st.button("🎶 Generate Music", use_container_width=True):

    if not prompt.strip():
        st.warning("Please enter a music prompt.")

    else:
        try:
            with st.spinner(
                "Loading model and generating music. Please wait..."
            ):
                generator = load_music_model()

                result = generator(
                    prompt,
                    forward_params={
                        "do_sample": True,
                        "max_new_tokens": duration_tokens
                    }
                )

                audio = result["audio"]
                sampling_rate = result["sampling_rate"]

                # Remove extra batch dimension when present
                if getattr(audio, "ndim", 1) > 1:
                    audio = audio.squeeze()

                sf.write(
                    str(OUTPUT_FILE),
                    audio,
                    sampling_rate
                )

            st.success("Music generated successfully! 🎉")

            st.audio(
                str(OUTPUT_FILE),
                format="audio/wav"
            )

            with open(OUTPUT_FILE, "rb") as audio_file:
                st.download_button(
                    label="⬇️ Download Generated Music",
                    data=audio_file,
                    file_name="generated_music.wav",
                    mime="audio/wav",
                    use_container_width=True
                )

        except Exception as error:
            st.error(f"Music generation failed: {error}")

st.divider()

st.subheader("Prompt Examples")

st.code("A calm piano melody for meditation")
st.code("Epic cinematic orchestral background music")
st.code("Happy acoustic guitar music with soft drums")
st.code("Relaxing lo-fi music for studying")