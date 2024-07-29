import requests
import logging
from config import WHISPER_ENDPOINT

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