#VoiceBot UI with Gradio
import os
import gradio as gr
from PIL import Image
import base64
from io import BytesIO
import uuid



# Import functions (ensure these are correctly defined in your project)
from brain_of_bot import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_medical_assistant import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# System prompt for the doctor
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# Helper function to encode the image
def encode_image(image_filepath):
    image = Image.open(image_filepath)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def process_inputs(audio_filepath, image_filepath):
    # Transcribe audio to text
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Process image if provided
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    # Generate speech response for the doctor
    output_filename = f"final_{str(uuid.uuid4())}.mp3"
    voice_of_doctorf = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=output_filename)

    return speech_to_text_output, doctor_response, voice_of_doctorf

# Create the Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Chatgpt Output"),
        gr.Audio()
    ], 
    title="AI Medibot with Vision and Voice"
)

# Launch the interface
iface.launch(debug=True)





#http://127.0.0.1:7863