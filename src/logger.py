import logging
import os


class Logger:

    def __init__(self, name, log_file_name, log_directory='./logs'):
        self._name = name
        self._log_file_name = log_file_name
        self.logger = logging.getLogger(self._name)
        self.logger.setLevel(logging.DEBUG)
        self.setup_logger()

    def setup_logger(self):
        self.delete_log_file()
        file_handler = logging.FileHandler(self._log_file_name)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    @staticmethod
    def create_log_directory(log_directory, log_file_name):
        """Function to create a log directory if it doesn't exist and return the log file path."""
        os.makedirs(log_directory, exist_ok=True)
        return os.path.join(log_directory, log_file_name)

    def delete_log_file(self):
        try:
            if os.path.exists(self._log_file_name):
                os.remove(self._log_file_name)
        except OSError as e:
            self.error(f"Failed to delete log file: {str(e)}")

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
