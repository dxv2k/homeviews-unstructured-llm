import os 
from typing import Any
from src.constants import * 


def prepare_project_dir(logger: Any) -> None:
    if not os.path.exists(OPENAI_EMBEDDINGS_FOLDER_PATH):
        logger.info(f"created {OPENAI_EMBEDDINGS_FOLDER_PATH}")
        os.mkdir(OPENAI_EMBEDDINGS_FOLDER_PATH)

    if not os.path.exists(SAVE_DIR):
        logger.info(f"created {SAVE_DIR}")
        os.mkdir(SAVE_DIR)

