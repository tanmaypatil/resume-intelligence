import io
import os
import json
from dotenv import load_dotenv
import json
import threading
import time
import websocket
import signal
import logging 
import base64
import pyaudio
import numpy as np
import wave
sample_rate=24000
audio_fragments = []

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



def is_json(value):
    if isinstance(value, str):
        try:
            json_object = json.loads(value)
            return True, json_object
        except json.JSONDecodeError:
            return False, None
    elif isinstance(value, (dict, list)):
        try:
            json_string = json.dumps(value)
            return True, value
        except TypeError:
            return False, None
    else:
        return False, None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global variable to control the WebSocket loop
websocket_running = True

load_dotenv()

# Ensure you have set your OpenAI API key in your environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# WebSocket URL for the real-time API
WS_URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"

def stitch_pcm16_audio(base64_fragments, sample_rate=24000):
    # Step 1: Decode base64 fragments
    raw_audio_fragments = [base64.b64decode(fragment) for fragment in base64_fragments]
    
    # Step 2: Concatenate raw audio data
    combined_audio = b''.join(raw_audio_fragments)
    
    # Step 3: Create a WAV file in memory
    with io.BytesIO() as wav_file:
        with wave.open(wav_file, 'wb') as wav:
            wav.setnchannels(1)  # Mono audio
            wav.setsampwidth(2)  # 2 bytes per sample for 16-bit audio
            wav.setframerate(sample_rate)
            wav.writeframes(combined_audio)
        
        # Get the WAV file content
        wav_data = wav_file.getvalue()
    
    # Step 4: Encode the WAV file as base64
    complete_base64_audio = base64.b64encode(wav_data).decode('utf-8')
    
    return complete_base64_audio

def on_message(ws, message):
    #print(f"Received message: {message}")
    flag,value = is_json(message)
    if flag:
      print(f"on_message : {value['type']}")
      type = value['type']
   
    if type and ( type == 'response.audio.delta'):
        #print(f"message is {message}")
        audio_delta = value['delta']
        audio_fragments.append(audio_delta)
    elif(type and ( type == 'response.audio.done')):
         print(f"message is {message}")
         enc_audio = stitch_pcm16_audio(audio_fragments)
         play_base64_pcm16_audio(enc_audio,sample_rate)
        
    ''' 
    if type and ( type == 'response.audio.delta')  :
      print(f"response.audio.done  : {value['delta'] , value['output_index'],value['content_index']}")
    elif type and ( type == 'response.audio.done')  :
        print(f"response.audio.done  :  {value['output_index'],value['content_index']}")
    '''

def on_error(ws, error):
    print(f"Error occurred: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Connection closed (status code: {close_status_code}, message: {close_msg})")

def on_open(ws):
    text = 'what is the day of week today'
    print("Connection opened") 
    # Example: sending a message after connection is established
    event = {
        "type": "conversation.item.create", 
        "item": {
            "type": "message",
            "role": "user",
            "content": [{
                "type": "input_text", 
                "text": text
            }]
        }
    }
    ws.send(json.dumps(event))
    #Ask for response 
    event_res = {
    "event_id": "event_234",
    "type": "response.create",
    "response": {
        "modalities": [ "text","audio"],
        "instructions": "Please assist the user",
        "voice": "alloy",
        "output_audio_format": "pcm16",
        "temperature": 0.7,
        "max_output_tokens": 150
      }
    }
    ws.send(json.dumps(event_res))

def signal_handler(signum, frame):
    global websocket_running
    logger.info("Interrupt received, closing connection...")
    websocket_running = False
    if ws:
        ws.close()

def run_websocket():
    global ws,websocket_running
    #websocket.enableTrace(True)  # For debugging, set to False in production
     # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    header = { 
        "OpenAI-Beta": "realtime=v1",
        "Authorization": "Bearer " +  OPENAI_API_KEY
    }
    ws = websocket.WebSocketApp(WS_URL,
                                header = header,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    while websocket_running:
        try:
          ws.run_forever()
          if not websocket_running:
              break
          logger.info("Connection lost. Attempting to reconnect in 5 seconds...")
          time.sleep(5)
        except Exception as e:
           logger.error(f"Error in WebSocket connection: {e}")
           if websocket_running:
             logger.info("Attempting to reconnect in 5 seconds...")
             time.sleep(5)
           else:
              break
    
    
def close_websocket():
    global websocket_running
    websocket_running = False
    print("Closing WebSocket connection...") 

if __name__ == "__main__":
  try:
    run_websocket()
  except KeyboardInterrupt:
    print("Program interrupted")
  finally:
    if ws:
      ws.close()  
       