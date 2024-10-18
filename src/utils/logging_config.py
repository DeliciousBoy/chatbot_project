import sys
from pathlib import Path
from loguru import logger

# Remove default logger to avoid clutter in the console
logger.remove()

# Create log directory if it doesn't exist
log_dir = Path('logs')
log_dir.mkdir(parents=True, exist_ok=True)

# Add new logger for stdout (console output) with 'INFO' and above
logger.add(sys.stdout, level="INFO")

def filter_success(record):
    return "Scraping" in record["message"] and record["level"].name == "SUCCESS"

logger.add(log_dir/ "scraping.log", retention='30 days', level='INFO')
logger.add(log_dir/  "success.log", retention='30 days', level='SUCCESS', filter=filter_success)
logger.add(log_dir/ "error.log", retention='30 days', level='ERROR')
logger.add(log_dir/ "warning.log", retention='30 days', level='WARNING')

