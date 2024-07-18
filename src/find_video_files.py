import os;

def find_video_files(directory, extensions=['.mp4', '.avi', '.mkv']):
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                video_files.append(os.path.join(root, file))
    return video_files