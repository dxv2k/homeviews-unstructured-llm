import os 
from typing import Any
from src.constants import * 


def prepare_project_dir(logger: Any) -> None:
    if not os.path.exists(OPENAI_EMBEDDINGS_FOLDER_PATH):
        logger.info(f"created {OPENAI_EMBEDDINGS_FOLDER_PATH}")
        os.mkdir(OPENAI_EMBEDDINGS_FOLDER_PATH)

    if not os.path.exists(UPLOAD_FOLDER):
        logger.info(f"created {UPLOAD_FOLDER}")
        os.mkdir(UPLOAD_FOLDER)

    if not os.path.exists(CSV_STORAGE_FOLDER):
        logger.info(f"created {CSV_STORAGE_FOLDER}")
        os.mkdir(CSV_STORAGE_FOLDER)

