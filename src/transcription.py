import whisper
import os
from src.cooling_time import time, cooling_time

# testing whisper AI model with test data
# # Load the Whisper model
# model = whisper.load_model("base")

# # Transcribe the audio file
# result = model.transcribe("/Users/jaswanth/Jaswanth_Workspace/How To Have A Healthy Relationship With Money [TYqZaqKcOwg].mp3")

# # Print the transcription
# print(result["text"])

def transcribe_audio(audio_path, transcription):

    model = whisper.load_model(transcription['model'])
    result = model.transcribe(audio_path)
    return result['text']

# transcriptions = {}

def transcribe_audios(audio_files, output_dir, transcriptionMode, update_progress):
    for audio_file in audio_files:
         # Extract filename without extension
        filename, _ = os.path.splitext(os.path.basename(audio_file))

        # Build the output transcript filename
        output_filename = os.path.join(output_dir, f"{filename}.txt")
        transcription = transcribe_audio(audio_file, transcriptionMode)

        # Save transcript to output file
        with open(output_filename, 'w') as f:
            f.write(transcription)

        if update_progress:
            update_progress(filename) 
        # Cooling time
        time.sleep(cooling_time)