import os
import shutil
import logging
from datetime import datetime

log_filename = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.info("File Automation Script Started")

folder_path = input("Enter the folder path to automate: ").strip()

if not os.path.isdir(folder_path):
    logger.error(f"Invalid folder path: {folder_path}")
    print("Folder not found. Please check the path and try again.")
    exit()

prefix = input("Enter a prefix for renaming files (e.g. backup): ").strip()

if not prefix:
    logger.warning("No prefix entered. Skipping rename operation.")
else:
    logger.info("Starting rename operation...")
    for filename in os.listdir(folder_path):
        try:
            old_path = os.path.join(folder_path, filename)
            if os.path.isfile(old_path) and not filename.startswith(prefix):
                new_filename = prefix + "_" + filename
                new_path = os.path.join(folder_path, new_filename)
                os.rename(old_path, new_path)
                logger.info(f"Renamed: {filename} -> {new_filename}")
        except Exception as e:
            logger.error(f"Error renaming {filename}: {e}")

logger.info("Starting sort by extension operation...")
for filename in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            ext_folder = ext.lstrip(".").upper() if ext else "NO_EXTENSION"
            dest_folder = os.path.join(folder_path, ext_folder)
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(dest_folder, filename))
            logger.info(f"Moved: {filename} -> {ext_folder}/")
    except Exception as e:
        logger.error(f"Error sorting {filename}: {e}")

logger.info("Starting clean operation (removing empty files)...")
for filename in os.listdir(folder_path):
    try:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
            os.remove(file_path)
            logger.info(f"Deleted empty file: {filename}")
    except Exception as e:
        logger.error(f"Error deleting {filename}: {e}")

logger.info("All operations completed successfully.")
print(f"\nDone! Log saved to: {log_filename}")
