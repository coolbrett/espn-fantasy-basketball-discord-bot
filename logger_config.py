import logging
import colorlog
import sys

# Define custom log colors for log levels
log_colors = {
    "DEBUG": "cyan",
    "INFO": "bold_blue",  # Bold blue for "INFO"
    "WARNING": "bold_yellow",
    "ERROR": "bold_red",
    "CRITICAL": "bold_red",
}

# Define the format with inline ANSI escape codes for colors
log_formatter = colorlog.ColoredFormatter(
    "\033[1;90m%(asctime)s\033[0m %(log_color)s%(levelname)-8s\033[0m \033[35m%(name)s\033[0m %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors=log_colors,
    reset=True,
)

# Create a global logger instance
logger = logging.getLogger("bot")
if not logger.hasHandlers():  # Ensure handlers are not duplicated
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(log_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
