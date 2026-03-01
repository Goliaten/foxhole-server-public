import glob
from importlib import import_module
import os
from typing import List
from fastapi import APIRouter

from src.core.Logger import Logger

excluded_files: List[str] = ["__init__.py"]
import_path = "src.api.war_support_live"
path = import_path.replace(".", os.sep)

Logger().get().debug("Importing war_support_live endpoints")
router = APIRouter()
for module in glob.glob(os.path.join(path, "*.py")):
    file = os.path.split(module)[-1]
    if file in excluded_files:
        continue

    import_name = f"{import_path}.{file[:-3]}"
    Logger().get().debug(f"Importing module: {module} {import_name}")
    try:
        imported_module = import_module(import_name)

        router.include_router(imported_module.router)
        Logger().get().debug("Included router")
    except AttributeError:
        Logger().get().error(f"Failed to import {file} module's router.")
        import traceback

        Logger().get().debug(traceback.format_exc())
