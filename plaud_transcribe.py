import os
import subprocess
import requests
import shutil
from pathlib import Path
from datetime import datetime
import json
import hashlib
import logging
from pydub import AudioSegment
from pydub.silence import split_on_silence
import webrtcvad
import wave
import contextlib

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants (consider moving to a config file)
PLAUD_NOTE_DIR = "/Volumes/PLAUD_NOTE/NOTES"
USB_DISK_DIR = "/Volumes/USB DISK/RECORD"
OBSIDIAN_DIR = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/"
WAV_BACKUP_DIR = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/asr/wav"
WHISPER_ENDPOINT = "http://192.168.1.25:9020/asr"
OLLAMA_ENDPOINT = "http://192.168.1.25:11434/api/generate"
PROCESSED_FILES_LOG = os.path.join(OBSIDIAN_DIR, "processed_files.json")
MP3_DIR = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/asr/mp3"
TRANSCRIPT_DIR = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/asr/transcript"


os.makedirs(MP3_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)



def convert_wav_files():
    for wav_file in os.listdir(WAV_BACKUP_DIR):
        if wav_file.lower().endswith('.wav'):
            wav_path = os.path.join(WAV_BACKUP_DIR, wav_file)
            mp3_file = os.path.splitext(wav_file)[0] + '.mp3'
            mp3_path = os.path.join(MP3_DIR, mp3_file)
            
            if not os.path.exists(mp3_path):
                convert_wav_to_mp3(wav_path, mp3_path)

def process_mp3_files():
    for mp3_file in os.listdir(MP3_DIR):
        if mp3_file.lower().endswith('.mp3'):
            mp3_path = os.path.join(MP3_DIR, mp3_file)
            transcript_file = os.path.splitext(mp3_file)[0] + '.md'
            transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)
            
            if not os.path.exists(transcript_path):
                # Transcribe MP3
                transcript = transcribe_audio(mp3_path)
                
                # Generate summary and hashtags
                summary, hashtags = generate_summary_and_hashtags(transcript)
                
                # Write transcript to markdown file
                with open(transcript_path, 'w') as md_file:
                    md_file.write(f"# Transcript of {mp3_file}\n\n")
                    md_file.write(f"## Summary\n{summary}\n\n")
                    md_file.write(f"## Hashtags\n{' '.join(hashtags)}\n\n")
                    md_file.write(f"## Full Transcript\n{transcript}")
                
                logging.info(f"Processed and transcribed: {mp3_file}")


def move_files_to_backup():
    moved_files = []
    directories = [PLAUD_NOTE_DIR, USB_DISK_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            logging.warning(f"Directory does not exist: {directory}")
            continue
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




def backup_obsidian():
    source_dir = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/"
    backup_dir = "/Volumes/DataMcDataFace/Obsidian/"
    
    if not os.path.exists(os.path.dirname(backup_dir)):
        logging.warning("Backup drive not connected. Skipping Obsidian backup.")
        return
    
    rsync_command = [
        "rsync",
        "-av",
        "--delete",
        source_dir,
        backup_dir
    ]
    try:
        subprocess.run(rsync_command, check=True)
        logging.info("Obsidian backup completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during Obsidian backup: {e}")


def convert_wav_to_mp3(wav_path, mp3_path):
    try:
        # Load the WAV file
        audio = AudioSegment.from_wav(wav_path)
        
        # Split audio on silence
        chunks = split_on_silence(
            audio,
            min_silence_len=500,  # Adjust this value (in ms) as needed
            silence_thresh=-40    # Adjust this value (in dB) as needed
        )
        
        # Concatenate chunks with short silences between them
        processed_audio = AudioSegment.empty()
        for chunk in chunks:
            processed_audio += chunk + AudioSegment.silent(duration=200)
        
        # Export as MP3
        processed_audio.export(mp3_path, format="mp3")
        
        logging.info(f"Converted and VAD-processed {wav_path} to {mp3_path}")
    except Exception as e:
        logging.error(f"Error converting {wav_path} to MP3: {e}")


def transcribe_audio(audio_path):
    try:
        with open(audio_path, 'rb') as audio_file:
            files = {'audio_file': audio_file}
            response = requests.post(WHISPER_ENDPOINT, files=files)
        logging.info(f"Transcription response status code: {response.status_code}")
        if response.status_code == 200:
            try:
                return response.json()['text']
            except requests.exceptions.JSONDecodeError:
                return response.text.strip()
        else:
            logging.error(f"Transcription failed with status code {response.status_code}")
            return f"Transcription failed with status code {response.status_code}"
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return f"Transcription error: {str(e)}"

def generate_summary_and_hashtags(transcript):
    prompt = f"""Based on the following transcript, provide a short summary (2-3 sentences) and generate 3-5 relevant hashtags. Format the output as JSON with 'summary' and 'hashtags' keys.

Transcript:
{transcript}

Output format:
{{
  "summary": "Your summary here",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}}
"""
    
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload)
        
        if response.status_code == 200:
            try:
                result = json.loads(response.json()['response'])
                return result['summary'], result['hashtags']
            except json.JSONDecodeError:
                logging.error("Failed to parse LLM response as JSON")
                return "", []
        else:
            logging.error(f"LLM processing failed with status code {response.status_code}")
            return "", []
    except Exception as e:
        logging.error(f"Error during LLM processing: {e}")
        return "", []

def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error generating hash for {file_path}: {e}")
        return None

def load_processed_files():
    if os.path.exists(PROCESSED_FILES_LOG):
        try:
            with open(PROCESSED_FILES_LOG, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Error parsing {PROCESSED_FILES_LOG}. Starting with empty processed files list.")
    return {}

def save_processed_files(processed_files):
    try:
        with open(PROCESSED_FILES_LOG, 'w') as f:
            json.dump(processed_files, f, indent=2)
        logging.info("Updated processed files log.")
    except Exception as e:
        logging.error(f"Error saving processed files log: {e}")

def is_file_processed(file_path, processed_files):
    file_hash = get_file_hash(file_path)
    return file_hash in processed_files if file_hash else False

def main():
    logging.info("Starting file backup process...")
    moved_files = move_files_to_backup()
    logging.info(f"Moved {len(moved_files)} files to backup folder.")
    logging.info("You can now unplug your recording device.")
    
    input("Press Enter to continue with processing...")
    
    logging.info("Starting WAV to MP3 conversion...")
    convert_wav_files()
    
    logging.info("Starting MP3 transcription...")
    process_mp3_files()
    
    logging.info("Attempting Obsidian backup...")
    backup_obsidian()
    
    logging.info("All operations completed.")



if __name__ == "__main__":
    main()
