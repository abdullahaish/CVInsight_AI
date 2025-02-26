import os
import logging

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Constructing file paths using os.path.join
debug_log_path = os.path.join("logs", "debug.log")
info_log_path = os.path.join("logs", "info.log")
warning_log_path = os.path.join("logs", "warning.log")

# Setting up the file handlers with the constructed paths
logging.basicConfig(
    handlers=[
        logging.FileHandler(debug_log_path),
        logging.FileHandler(info_log_path),
        logging.FileHandler(warning_log_path)
    ],
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)