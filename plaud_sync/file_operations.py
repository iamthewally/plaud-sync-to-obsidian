import os
import shutil
import logging
import subprocess
from config import WAV_BACKUP_DIR, MP3_DIR, TRANSCRIPT_DIR, SUMMARY_DIR

def ensure_directories():
    for directory in [MP3_DIR, TRANSCRIPT_DIR, SUMMARY_DIR]:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Ensured directory exists: {directory}")

def move_files_to_backup(directories):
    """Moves WAV files from specified directories to a backup directory."""
    moved_files = []
    for directory in directories:
        if not os.path.exists(directory):
            logging.warning(f"Directory does not exist: {directory}")
            continue
        
        # Walk through all subdirectories within the provided directory
        for root, _, files in os.walk(directory):
            if root == WAV_BACKUP_DIR:
                continue  # Skip the backup directory itself
            for file in files:
                if file.lower().endswith('.wav'):
                    source_path = os.path.join(root, file)
                    dest_path = os.path.join(WAV_BACKUP_DIR, file)                 
                    counter = 1
                    base_name, ext = os.path.splitext(file)
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(WAV_BACKUP_DIR, f"{base_name}_{counter}{ext}")
                        counter += 1
                    
                    try:
                        shutil.move(source_path, dest_path)
                        moved_files.append(dest_path)
                        logging.info(f"Moved {source_path} to {dest_path}")
                    except Exception as e:
                        logging.error(f"Error moving file {source_path}: {e}")
    
    return moved_files

def ensure_directories():
    for directory in [MP3_DIR, TRANSCRIPT_DIR]:
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Ensured directory exists: {directory}")



def convert_wav_to_mp3(wav_path, mp3_path):
    from config import MP3_BITRATE
    
    command = ['ffmpeg', '-i', wav_path, '-acodec', 'libmp3lame', '-b:a', MP3_BITRATE, '-loglevel', 'error', mp3_path]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {wav_path} to MP3: {e.stderr}")

def convert_wav_files(progress_callback=None):
    wav_files = [f for f in os.listdir(WAV_BACKUP_DIR) if f.lower().endswith('.wav')]
    total_files = len(wav_files)
    
    for index, wav_file in enumerate(wav_files, start=1):
        wav_path = os.path.join(WAV_BACKUP_DIR, wav_file)
        mp3_file = os.path.splitext(wav_file)[0] + '.mp3'
        mp3_path = os.path.join(MP3_DIR, mp3_file)
        if not os.path.exists(mp3_path):
            convert_wav_to_mp3(wav_path, mp3_path)
        
        if progress_callback:
            progress_callback(index, total_files)
