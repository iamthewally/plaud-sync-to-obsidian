# Plaud Sync to Obsidian

This script automates the process of syncing audio recordings from Plaud Note devices to Obsidian, including transcription, summarization, and backup.  Workflow and setup is very custom to my environment at the moment, but it might be helpful for others with a bit of polish.  The device appears as an external disk when connected to USB, so there is no real magic in grabbing those files.  I have a second folder location configurable for more files, as I sometimes have recording made in Obsidian itself that I want to process.  

Transcription is currently via a Whisper endpoint on a personal server.  https://github.com/ahmetoner/whisper-asr-webservice

Summaries are handled by an Ollama instance on the same personal server as the transcription. I'm using a GGUF of Command R for the model and it has been working like a champ for summarization at 32K context.  https://huggingface.co/CohereForAI/c4ai-command-r-08-2024

## Functions (in process order)

1. Moves WAV files from Plaud Note devices to a backup directory
2. Converts WAV files to MP3 format
3. Generates transcriptions using a Whisper endpoint (https://github.com/ahmetoner/whisper-asr-webservice)
4. Generates summaries with hashtags using an Ollama endpoint (https://github.com/ollama/ollama)
5. Place summaries and transcripts directly into an Obsidian vault!

## Screenshots
1. Summary note in Obsidian
![image](https://github.com/user-attachments/assets/cc46e3fd-3161-4bb7-b5cb-b891ee68fec1)
2. Transcript in Obsidian
![image](https://github.com/user-attachments/assets/7cbcdf84-ecd2-4efc-a66b-2b1e6448cb75)

## Todo

- Make configuration friendlier
- Break summarization into N steps for more focused prompting (prompt for just the where, prompt for just when, etc)
- Include local Ollama
- Include local Whisper (WhisperX?)
- Support other ASR/LLM endpoints
- Diarization

## Project Structure

```
project_root/
│
├── config.py
├── main.py
├── requirements.txt
├── README.md
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
3. Configure the paths and API parameters in `config.py`
4. Adjust prompt for summary by LLM in summarization.py

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
