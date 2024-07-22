def generate_combined_transcript(transcriptions, output_path):
    with open(output_path, 'w') as f:
        for file, text in transcriptions.items():
            f.write(f"\n{text}\n\n")