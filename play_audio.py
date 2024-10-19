import numpy as np
import base64
import pyaudio
import struct

def generate_sine_wave(freq, duration, sample_rate=8000, amplitude=32767):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sine_wave = amplitude * np.sin(2 * np.pi * freq * t)
    return sine_wave.astype(np.int16)

def play_audio(audio_data, sample_rate=8000, channels=1):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    output=True)
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()

# Generate a 2-second 440 Hz sine wave
sample_rate = 8000
duration = 2
frequency = 440
audio_data = generate_sine_wave(frequency, duration, sample_rate)

# Convert to bytes
audio_bytes = audio_data.tobytes()

# Encode to base64
base64_audio = base64.b64encode(audio_bytes).decode('utf-8')

print("Base64 encoded PCM16 audio (2 seconds, 440 Hz sine wave, 8000 Hz sample rate):")
print(base64_audio)
print(f"\nLength of base64 string: {len(base64_audio)}")

# Function to play base64 encoded audio
def play_base64_pcm16_audio(base64_audio, sample_rate=8000, channels=1):
    try:
        audio_data = base64.b64decode(base64_audio)
        play_audio(audio_data, sample_rate, channels)
        print("Audio playback completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Play the audio
print("\nPlaying the audio...")
play_base64_pcm16_audio(base64_audio, sample_rate=8000)