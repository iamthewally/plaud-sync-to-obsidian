import hashlib
import json
import logging
import os
from config import PROCESSED_FILES_LOG

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_processed_files():
    try:
        with open(PROCESSED_FILES_LOG, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_processed_files(processed_files):
    with open(PROCESSED_FILES_LOG, 'w') as f:
        json.dump(processed_files, f, indent=2)

def is_file_processed(file_path, processed_files):
    file_hash = get_file_hash(file_path)
    return file_hash in processed_files if file_hash else False