import hashlib
import json
import logging
import os
from config import PROCESSED_FILES_LOG

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