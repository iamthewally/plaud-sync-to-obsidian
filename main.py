# main.py

import click
import logging
import os
from config import MP3_DIR, TRANSCRIPT_DIR, SUMMARY_DIR, PLAUD_NOTE_DIR, USB_DISK_DIR, WAV_BACKUP_DIR, LOG_FORMAT, LOG_LEVEL
from plaud_sync.file_operations import move_files_to_backup, ensure_directories, convert_wav_files
from plaud_sync.transcription import transcribe_audio
from plaud_sync.summarization import generate_summary
from plaud_sync.backup import backup_obsidian
from plaud_sync.utils import load_processed_files, save_processed_files, is_file_processed

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

@click.command()
def sync():
    """Sync Plaud Note recordings to Obsidian"""
    try:
        click.echo("Starting Plaud Sync process...")

        # Step 1: Backup files
        click.echo("Backing up files...")
        moved_files = move_files_to_backup([PLAUD_NOTE_DIR, USB_DISK_DIR])
        click.echo(f"Moved {len(moved_files)} files to backup folder.")

        # Step 2: Convert WAV to MP3
        click.echo("Converting WAV files to MP3...")
        ensure_directories()
        convert_wav_files(progress_callback=lambda completed, total: click.echo(f"Converted {completed}/{total} files", nl=False))

        # Step 3: Transcribe MP3 files
        click.echo("\nTranscribing MP3 files...")
        transcribe_mp3_files()

        # Step 4: Generate summaries from transcripts
        click.echo("Generating summaries...")
        generate_summaries()

        # Step 5: Backup Obsidian vault
        click.echo("Backing up Obsidian vault...")
        backup_obsidian()

        click.echo(click.style("All operations completed successfully.", fg="green"))
    except KeyboardInterrupt:
        click.echo(click.style("\nOperation cancelled by user. Exiting.", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"An error occurred: {str(e)}", fg="red"))
        logger.exception("An error occurred during sync process")

def transcribe_mp3_files():
    processed_files = load_processed_files()
    mp3_files = [f for f in os.listdir(MP3_DIR) if f.lower().endswith('.mp3')]
    total_mp3_files = len(mp3_files)
    
    with click.progressbar(mp3_files, label="Transcribing MP3 files") as bar:
        for mp3_file in bar:
            mp3_path = os.path.join(MP3_DIR, mp3_file)
            transcript_file = os.path.splitext(mp3_file)[0] + '.md'
            transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)
            
            if not is_file_processed(mp3_path, processed_files):
                try:
                    transcript = transcribe_audio(mp3_path)
                    with open(transcript_path, 'w') as md_file:
                        md_file.write(f"# Transcript of {mp3_file}\n\n{transcript}")
                    processed_files[mp3_path] = True
                except Exception as e:
                    click.echo(click.style(f"\nError transcribing {mp3_file}: {e}", fg="red"))
    
    save_processed_files(processed_files)

def generate_summaries():
    transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.lower().endswith('.md')]
    total_files = len(transcript_files)
    
    with click.progressbar(transcript_files, label="Generating summaries") as bar:
        for transcript_file in bar:
            transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)
            summary_file = transcript_file
            summary_path = os.path.join(SUMMARY_DIR, summary_file)
            
            if not os.path.exists(summary_path):
                try:
                    with open(transcript_path, 'r') as f:
                        transcript = f.read()
                    summary = generate_summary(transcript)
                    with open(summary_path, 'w') as f:
                        f.write(summary)
                except Exception as e:
                    click.echo(click.style(f"\nError generating summary for {transcript_file}: {e}", fg="red"))

if __name__ == "__main__":
    sync()
