from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

PROJ_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = PROJ_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
# logger.info(f"PROJ_ROOT path is: {PROJ_DIR}")

def in_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other types
    except NameError:
        return False  # Probably standard Python interpreter

try:
    from tqdm import tqdm
    # Remove default handler if not in Jupyter environment
    if not in_notebook():
        logger.remove(0)
    # logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass


