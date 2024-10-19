import pyttsx3
import pyaudio
import wave
import io
import base64
import numpy as np
import os

def text_to_high_quality_pcm16_base64(text, sample_rate=44100):
    engine = pyttsx3.init()
    
    # Set properties for better quality
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Try to use a better voice if available
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower() and "high" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    else:
        # If no high-quality voice found, use the default
        print("No high-quality voice found. Using default voice.")

    # Create a temporary file
    temp_file = 'temp_high_quality_audio.wav'

    # Save speech to the temporary file
    engine.save_to_file(text, temp_file)
    engine.runAndWait()

    # Read the saved file and convert to PCM16
    with wave.open(temp_file, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        pcm_data = wf.readframes(n_frames)

    # Remove the temporary file
    os.remove(temp_file)

    # Convert to numpy array
    audio_array = np.frombuffer(pcm_data, dtype=np.int16)

    # Resample to desired sample rate if necessary
    if framerate != sample_rate:
        audio_array = np.interp(
            np.linspace(0, len(audio_array), int(len(audio_array) * sample_rate / framerate)),
            np.arange(len(audio_array)),
            audio_array
        ).astype(np.int16)

    # Encode to base64
    base64_audio = base64.b64encode(audio_array.tobytes()).decode('utf-8')
    
    return base64_audio, sample_rate

def play_base64_pcm16_audio(base64_audio, sample_rate):
    # Decode base64 string
    audio_data = base64.b64decode(base64_audio)
    
    # Convert to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Play the audio
    stream.write(audio_array.tobytes())

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()

# Generate the audio
text = "Roger Federer is the tennis player I like the most."
print(f"Generating high-quality PCM16 audio for: '{text}'")
base64_audio, sample_rate = text_to_high_quality_pcm16_base64(text)
print("High-quality audio generated and encoded to base64.")

# Print the full base64 string
print("\nFull base64 encoded PCM16 audio:")
print(base64_audio)

print(f"\nSample rate: {sample_rate} Hz")

# Play the audio
print("\nPlaying the generated audio...")
play_base64_pcm16_audio(base64_audio, sample_rate)
print("Audio playback completed.")