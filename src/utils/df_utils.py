import io 
import pandas as pd 
from src.constants import CSV_STORAGE_FOLDER
from src.utils.logger import get_logger

logger = get_logger()


def string_to_df(value: str, seperator: str = "\t") -> pd.DataFrame | ValueError: 
    try: 
        df = pd.read_csv(io.StringIO(value), sep=seperator)
        return df  
    except Exception as e: 
        logger.info(f"Exception occured while string_to_df with value: {value}, exception: {e}")
        raise ValueError("Unable to parse the data, see logs for more info")


def save_df_to_csv(
    df: pd.DataFrame, 
    filename: str, 
    sepeator: str = "\t"
) -> str: 
    _path = f"{CSV_STORAGE_FOLDER}/{filename}.csv"
    df.to_csv(_path, sep=sepeator, encoding="utf-8") 
    return _path