import openai
import pyaudio
import wave
import io
import json

# Initialize OpenAI client
client = openai.OpenAI()

# Audio recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def get_current_weather(location, unit="celsius"):
    """Mock function to get current weather"""
    weather_info = {
        "location": location,
        "temperature": "22",
        "unit": unit,
        "forecast": ["sunny", "windy"]
    }
    return json.dumps(weather_info)

# Define available functions
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * 5)):  # 5 seconds of audio
        data = stream.read(CHUNK)
        frames.append(data)
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = io.BytesIO()
    wf = wave.open(audio_data, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    audio_data.seek(0)
    return audio_data

def play_audio(audio_stream):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    
    chunk = audio_stream.read(CHUNK)
    while chunk:
        stream.write(chunk)
        chunk = audio_stream.read(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

def interact_with_realtime_api():
    while True:
        print("Press Enter to start speaking...")
        input()
        audio_input = record_audio()

        try:
            response = client.audio.speech.create(
                model="whisper-1",
                file=audio_input,
                response_format="text"
            )
            print(f"You said: {response}")

            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": response}],
                stream=True,
                functions=functions,
                function_call="auto"
            )

            full_response = ""
            function_call = None
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                if chunk.choices[0].delta.function_call:
                    function_call = chunk.choices[0].delta.function_call

            if function_call:
                function_name = function_call.name
                function_args = json.loads(function_call.arguments)
                if function_name == "get_current_weather":
                    function_response = get_current_weather(**function_args)
                    full_response += f"\nWeather info: {function_response}"
                else:
                    full_response += f"\nUnknown function: {function_name}"

            print(f"Assistant: {full_response}")

            audio_output = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=full_response
            )

            audio_output.stream_to_file("response.mp3")
            with wave.open("response.mp3", "rb") as wf:
                play_audio(wf)

        except Exception as e:
            print(f"An error occurred: {e}")

        print("Continue? (y/n)")
        if input().lower() != 'y':
            break

if __name__ == "__main__":
    interact_with_realtime_api()