from pathlib import Path

import config
from src.core.Logger import Logger


def setup():
    dirs = [config.LOG_DIR]
    for directory in dirs:
        Path(directory).mkdir(exist_ok=True, parents=True)
    Logger().get().debug("Setup finished")
