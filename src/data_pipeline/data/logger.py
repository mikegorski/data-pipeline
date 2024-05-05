import logging
from datetime import datetime
from pathlib import Path

from data_pipeline.settings import LOG_DIR


class Logger:
    def __init__(self, name: str, log_dir: Path = LOG_DIR):
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file_handler = None

    def set_file_handler(self):
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_name = f"log_{current_datetime}.txt"
        log_file_path = self.log_dir / log_file_name
        self.file_handler = logging.FileHandler(log_file_path)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def log_error(self, message):
        if not self.file_handler:
            self.set_file_handler()
        self.logger.error(message)

    def log_info(self, message):
        if not self.file_handler:
            self.set_file_handler()
        self.logger.info(message)
