import os
import sys
import yaml
import logging
import time
from tqdm import tqdm
from src.generate_instruction_completion_datasets import generate_instruction_completion_dataset

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Diagnostic prints
print("Current working directory:", os.getcwd())
print("Contents of current directory:", os.listdir())
print("Python path:", sys.path)

if os.path.exists('src'):
    print("Contents of src directory:", os.listdir('src'))
    print("Full path of src directory:", os.path.abspath('src'))
else:
    print("src directory does not exist")

# Now import the required modules
try:
    print("Attempting to import from src.video_to_audio...")
    from src.video_to_audio import process_media
    print("Successfully imported process_media from src.video_to_audio")
    from src.transcription import transcribe_audios, optimized_transcribe
    from src.generate_combined_transcript import generate_combined_transcript
    from src.utils import setup_logging, create_output_directories
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure the file names in the 'src' directory match the import statements.")
    print("Python is looking for modules in these locations:")
    for path in sys.path:
        print(f"  {path}")
    sys.exit(1)

def main():
    try:
        start_time = time.time()
        # Load configuration
        with open('config.yaml', 'r') as config_file:
            config = yaml.safe_load(config_file)

        # Setup logging
        logger = setup_logging(level=logging.INFO)

        # Create output directories
        output_dir = create_output_directories(config['directories']['output'])

        # Process media files
        logger.info(f"Starting media processing from {config['directories']['input']}")
        audio_files = process_media(config['directories']['input'], output_dir)
        print(f"Processed audio files: {audio_files}")
        logger.info(f"Processed audio files: {audio_files}")

        # Check if audio files were processed correctly
        if not audio_files:
            logger.error("No audio files processed. Check if the input directory contains media files.")
            sys.exit(1)

        # Transcribe audio files
        logger.info("Starting audio transcription")
        
        total_files = len(audio_files)
        with tqdm(total=total_files, desc="Overall Progress", unit="file") as pbar:
            def update_progress(future):
                pbar.update()
            
        # transcriptions = transcribe_audios(audio_files, output_dir, config['transcription'], update_progress)
        transcriptions = optimized_transcribe(audio_files, output_dir, config['transcription'], update_progress)

        logger.info("transcription process complete")

        # Merge generated transcripts
        logger.info("starting transcript merge")

        generate_combined_transcript(transcriptions, output_dir + '/combined_transcription.txt')
        logger.info("combined script generated")

        # generate instruction completion dataset
        instruction_completion_data = generate_instruction_completion_dataset(output_dir + '/combined_transcription.txt')
        with open(output_dir + '/chatGPT_output_file.txt', 'w') as file:
            file.write(instruction_completion_data)
        
        end_time = time.time()
        logger.info(f"Total time taken: {end_time - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
