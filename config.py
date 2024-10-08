# Constants and configuration variables

PLAUD_NOTE_DIR = "/Volumes/PLAUD_NOTE/NOTES"
USB_DISK_DIR = "/Volumes/USB DISK/RECORD"
OBSIDIAN_DIR = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/Primary"
WAV_BACKUP_DIR = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/Primary/asr/wav"
WHISPER_ENDPOINT = "http://192.168.1.25:9020/asr"
OLLAMA_ENDPOINT = "http://192.168.1.25:11434/api/generate"
PROCESSED_FILES_LOG = f"{OBSIDIAN_DIR}/processed_files.json"
MP3_DIR = f"{OBSIDIAN_DIR}/asr/mp3"
TRANSCRIPT_DIR = f"{OBSIDIAN_DIR}/asr/transcript"

# Backup configuration
OBSIDIAN_BACKUP_SOURCE = "/Users/wa/Library/Mobile Documents/iCloud~md~obsidian/Documents/"
OBSIDIAN_BACKUP_DEST = "/Volumes/DataMcDataFace/Obsidian/"
SUMMARY_DIR = f"{OBSIDIAN_DIR}/asr/summary"

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# API models
LLM_MODEL = "command-r:35b-08-2024-q4_K_M"

# WAV -> MP# conversion settings
MP3_BITRATE = '128k'