import subprocess
import os
from src.find_video_files import find_video_files

def convert_video_to_audio(video_path, output_path):
      # Extract filename and extension
    filename, extension = os.path.splitext(os.path.basename(video_path))

  # Create output filename with .mp3 extension
    output_filename = os.path.join(output_path + '/', f"{filename}.mp3")
    command = ['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', output_filename]
    subprocess.run(command)
    return output_filename

def process_media(input_dir, output_dir):
    audio_files = []
    for video_file in find_video_files(input_dir):
        # audio_file =  os.path.splitext(video_file)[0] + '.mp3'
        audio_files.append(convert_video_to_audio(video_file, output_dir)) 
    
    return audio_files
