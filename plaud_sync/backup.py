import os
import subprocess
import logging
from config import OBSIDIAN_BACKUP_SOURCE, OBSIDIAN_BACKUP_DEST

def backup_obsidian():
    if not os.path.exists(os.path.dirname(OBSIDIAN_BACKUP_DEST)):
        logging.warning("Backup drive not connected. Skipping Obsidian backup.")
        return
    
    rsync_command = [
        "rsync",
        "-av",
        "--delete",
        OBSIDIAN_BACKUP_SOURCE,
        OBSIDIAN_BACKUP_DEST
    ]
    try:
        subprocess.run(rsync_command, check=True)
        logging.info("Obsidian backup completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during Obsidian backup: {e}")