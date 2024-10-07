# Plaud Sync to Obsidian

This project automates the process of syncing audio recordings from Plaud Note devices to Obsidian, including transcription, summarization, and backup functionalities.

## Features

- Moves WAV files from Plaud Note devices to a backup directory
- Converts WAV files to MP3 format
- Transcribes audio files using a Whisper ASR API
- Generates summaries and hashtags for transcripts using an Ollama endpoint
- Creates markdown files with the transcripts, summaries, and hashtags
- Backs up Obsidian vault to an external drive

## Project Structure

```
project_root/
│
├── config.py
├── main.py
├── requirements.txt
├── README.md
│
└── plaud_sync/
    ├── file_operations.py
    ├── transcription.py
    ├── summarization.py
    ├── backup.py
    └── utils.py
```

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure the paths and API endpoints in `config.py`

## Usage

Run the main script:

```
python main.py
```

The script will guide you through the process of backing up files, transcribing audio, and creating markdown notes in your Obsidian vault.

## Dependencies

- Python 3.7+
- ffmpeg (for audio conversion)
- requests (for API calls)
- Other dependencies listed in `requirements.txt`