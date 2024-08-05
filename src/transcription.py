import whisper
import os
import logging
import concurrent.futures
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

transcriptions = {}

def transcribe_audios(audio_files, output_dir, transcription_mode, update_progress):
    for audio_file in audio_files:
         # Extract filename without extension
        filename, _ = os.path.splitext(os.path.basename(audio_file))

        # Build the output transcript filename
        output_filename = os.path.join(output_dir, f"{filename}.txt")
        transcriptions[audio_file] = transcribe_audio(audio_file, transcription_mode)

        # Save transcript to output file
        with open(output_filename, 'w') as f:
            f.write(transcriptions[audio_file])

        if update_progress:
            update_progress(filename) 
        # Cooling time
        time.sleep(cooling_time)
    return transcriptions

def trascribe_audio_file(audio_file):
        # Build the output transcript filename
        print(f"transcribing started for audio file {audio_file}")
        transcription_mode = { 'model':'base'}
        transcription = transcribe_audio(audio_file, transcription_mode)
        return transcription

def optimized_transcribe(audio_files, output_dir, transcription_mode, update_progress):
    # Process audio files concurrently
    with concurrent.futures.ProcessPoolExecutor() as executor:
        transcripts = list(executor.map(trascribe_audio_file, audio_files))
    
    # Output each transcript
    for i, transcript in enumerate(transcripts):
        # Extract filename without extension
        filename, _ = os.path.splitext(os.path.basename(audio_files[i]))
        output_filename = os.path.join(output_dir, f"{filename}.txt")
        transcriptions[audio_files[i]] = transcript
        # Save transcript to output file
        with open(output_filename, 'w') as f:
            f.write(transcript)
        if update_progress:
            update_progress(filename)

    return transcriptions