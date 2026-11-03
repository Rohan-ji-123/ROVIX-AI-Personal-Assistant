import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
DURATION = 8
DEVICE_ID = 0

model = None


def listen():
    global model

    # Load model only when listen() is called for the first time
    if model is None:
        print("ROVIX: Loading speech recognition model...")

        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        print("ROVIX: Speech recognition model loaded!")

    print(f"ROVIX: Listening... Speak now for {DURATION} seconds.")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=DEVICE_ID
    )

    sd.wait()
    audio = np.squeeze(audio)

    print("ROVIX: Processing speech...")

    segments, info = model.transcribe(
        audio,
        language="en",
        beam_size=5
    )

    text = " ".join(segment.text.strip() for segment in segments)

    if text:
        print("YOU:", text)
        return text

    print("ROVIX: I couldn't understand. Please try again.")
    return ""
