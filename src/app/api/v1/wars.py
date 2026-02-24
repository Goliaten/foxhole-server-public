import glob
from importlib import import_module
import os
from typing import List
from fastapi import APIRouter, logger

excluded_files: List[str] = ["__init__.py"]
import_path = "src.app.api.v1.endpoints"
path = import_path.replace(".", os.sep)


router = APIRouter()
for module in glob.glob(os.path.join(path, "*.py")):
    file = os.path.split(module)[-1]
    if file in excluded_files:
        continue

    try:
        imported_module = import_module(f"{import_path}.{file[:-3]}")

        router.include_router(imported_module.router)
    except AttributeError as e:
        logger.logger.error(f"Failed to import {file} module's router.")
        import traceback

        logger.logger.debug(traceback.format_exc())
