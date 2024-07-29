# Plaud Sync to Obsidian

This script processes WAV audio files from specified directories, converts them to MP3, transcribes them using a Whisper ASR service, and saves the transcriptions as markdown files in an Obsidian vault.

## Features

- Converts WAV files to MP3 for efficient processing
- Transcribes audio using a Whisper ASR service
- Saves transcriptions as markdown files in an Obsidian vault
- Processes files from multiple source directories
- Cleans up temporary MP3 files after processing

## Requirements

- Python 3.7+
- ffmpeg
- requests library

## Setup

1. Clone this repository
2. Install the required Python packages: `pip install -r requirements.txt`
3. Ensure ffmpeg is installed and available in your system PATH
4. Update the configuration in `config.py` with your specific paths and settings

## Usage

Run the script with:
```
python plaud_transcribe.py
```




## Configuration

Edit `config.py` to set the following variables:

- `PLAUD_NOTE_DIR`: Directory path for PLAUD_NOTE device
- `USB_DISK_DIR`: Directory path for USB DISK device
- `OBSIDIAN_DIR`: Directory path for your Obsidian vault
- `WHISPER_ENDPOINT`: URL of your Whisper ASR service

## License

[MIT License](LICENSE)