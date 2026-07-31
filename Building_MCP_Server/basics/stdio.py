import logging

logging.basicConfig(
    level=logging.INFO, # Set the logging level to INFO, which means that all messages at this level and above will be logged.
    format="%(levelname)s: %(message)s" # Set the format of the log messages to include the log level and the message itself.
)

logger = logging.getLogger(__name__)

# ❌ Bad (STDIO)
print("Processing request 1")  # writes to stdout

# ✅ Good (STDIO)
logger.info("Processing request 2")  # writes to stderr, which means it will be captured by the logging system and can be redirected to a file or other logging handlers.