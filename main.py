import logging
import os
from config import MP3_DIR, TRANSCRIPT_DIR, PLAUD_NOTE_DIR, USB_DISK_DIR, LOG_FORMAT, LOG_LEVEL
from plaud_sync.file_operations import move_files_to_backup, ensure_directories, convert_wav_files
from plaud_sync.transcription import transcribe_audio
from plaud_sync.summarization import generate_summary_and_hashtags
from plaud_sync.backup import backup_obsidian
from plaud_sync.utils import load_processed_files, save_processed_files, is_file_processed

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)

def process_mp3_files():
    processed_files = load_processed_files()
    for mp3_file in os.listdir(MP3_DIR):
        if mp3_file.lower().endswith('.mp3'):
            mp3_path = os.path.join(MP3_DIR, mp3_file)
            transcript_file = os.path.splitext(mp3_file)[0] + '.md'
            transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)
            
            if not is_file_processed(mp3_path, processed_files):
                try:
                    transcript = transcribe_audio(mp3_path)
                    summary, hashtags = generate_summary_and_hashtags(transcript)
                    
                    with open(transcript_path, 'w') as md_file:
                        md_file.write(f"# Transcript of {mp3_file}\n\n")
                        md_file.write(f"## Summary\n{summary}\n\n")
                        md_file.write(f"## Hashtags\n{' '.join(hashtags)}\n\n")
                        md_file.write(f"## Full Transcript\n{transcript}")
                    
                    logging.info(f"Processed and transcribed: {mp3_file}")
                    processed_files[mp3_path] = True
                except Exception as e:
                    logging.error(f"Error processing {mp3_file}: {e}")
    
    save_processed_files(processed_files)

def main():
    try:
        logging.info("Starting file backup process...")
        moved_files = move_files_to_backup([PLAUD_NOTE_DIR, USB_DISK_DIR])
        logging.info(f"Moved {len(moved_files)} files to backup folder.")
        logging.info("You can now unplug your recording device.")
        
        input("Press Enter to continue with processing...")
        
        ensure_directories()
        
        logging.info("Starting WAV to MP3 conversion...")
        convert_wav_files()
        
        logging.info("Starting MP3 transcription...")
        process_mp3_files()
        
        logging.info("Attempting Obsidian backup...")
        backup_obsidian()
        
        logging.info("All operations completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during the main process: {e}")
    finally:
        logging.info("Script execution finished.")

if __name__ == "__main__":
    main()