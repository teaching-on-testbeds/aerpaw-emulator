"""
This script provides a reusable logger setup for tracking events, errors, and runtime information,
with output to both a log file and the console. It uses a custom formatter that includes
timestamps with millisecond precision for accurate debugging and monitoring.

The logger is configured by calling the `setup_logger(log_file_path)` function from the calling script,
allowing full control over the log file name and location. This design supports flexible logging for
different use cases (e.g., TX, RX, testing sessions) while maintaining consistent formatting.

Features:
- Millisecond-resolution timestamps in log entries
- Dual output: logs to both file and console
- Clean integration into other scripts via import

Maintainer: Sergio Vargas <svargas3@ncsu.edu>
Last updated: 04-09-2025
"""

import logging
import os
from datetime import datetime


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            t = datetime.fromtimestamp(record.created)
            s = t.strftime("%H:%M:%S,%f")[:-3]
        return s


def setup_logger(log_file_path=None):
    if not logging.getLogger().hasHandlers():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handlers = []

        if log_file_path:
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.INFO)
            handlers.append(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        handlers.append(stream_handler)

        formatter = CustomFormatter("%(levelname)s - %(asctime)s - %(message)s", datefmt="%H:%M:%S,%f")

        for handler in handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)
