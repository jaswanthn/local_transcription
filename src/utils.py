import logging
import os


def setup_logging(level=logging.INFO):
  """

  Args:
      level (int, optional): The logging level. Defaults to logging.INFO.

  Returns:
      logging.Logger: The configured logger object.
  """

  handler = logging.FileHandler('transcription.log')
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler.setFormatter(formatter)

  logger = logging.getLogger('transcriptionLogger')
  logger.setLevel(level)
  logger.addHandler(handler)

  return logger


def create_output_directories(output_path):
  output_path = os.path.normpath(output_path)

  try:
    # Avoids raising errors if directory already exists
    os.makedirs(output_path, exist_ok=True)

    # Option 2: Using pathlib (Python 3.4+)
    # from pathlib import Path
    # Path(output_path).mkdir(parents=True, exist_ok=True)

  except OSError as e:
    raise OSError(
        f"Error creating output directory: {output_path}. Reason: {e}")

  return os.path.abspath(output_path)  # Return the absolute path
