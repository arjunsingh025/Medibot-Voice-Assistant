import os
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from playsound import playsound

# Step 1a: Setup Text-to-Speech with gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "hi"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    play_audio(output_filepath)

# Step 1b: Setup Text-to-Speech with ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    if not ELEVENLABS_API_KEY:
        print("Error: ELEVENLABS_API_KEY not found in environment variables.")
        return
    
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    
    # Check if the file is saved successfully
    if os.path.exists(output_filepath):
        print(f"Audio file saved as: {output_filepath}")
    else:
        print(f"Error: {output_filepath} was not created.")
    
    play_audio(output_filepath)

# Common function to play audio using playsound for MP3 support
def play_audio(output_filepath):
    try:
        if os.path.exists(output_filepath):
            print(f"Playing audio file: {output_filepath}")
            playsound(output_filepath)  # Plays the MP3 directly using playsound
        else:
            print(f"Error: {output_filepath} does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Example usage
input_text = "Hi, I am Arjun! Let's test Text-to-Speech conversion."

# Uncomment one of the following lines depending on which TTS method you want to use:
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing.mp3")
text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="elevenlabs_testing.mp3")

