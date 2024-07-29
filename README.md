# Plaud Sync to Obsidian

This project automates the process of syncing audio recordings from Plaud Note devices to Obsidian, including transcription, summarization, and backup functionalities.

## Features

- Moves WAV files from Plaud Note devices to a backup directory
- Converts WAV files to MP3 format
- Transcribes audio files using a Whisper ASR API
- Generates summaries and hashtags for transcripts using an LLM API
- Creates markdown files with transcripts, summaries, and hashtags
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
├── plaud_sync/
│   ├── __init__.py
│   ├── file_operations.py
│   ├── transcription.py
│   ├── summarization.py
│   ├── backup.py
│   └── utils.py
│
└── tests/
    ├── __init__.py
    ├── test_file_operations.py
    ├── test_transcription.py
    └── test_summarization.py
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

## Testing

To run the unit tests:

```
python -m unittest discover tests
```

## Dependencies

- Python 3.7+
- ffmpeg (for audio conversion)
- requests (for API calls)
- Other dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).