import os 

from src.constants import CSV_STORAGE_FOLDER, OPENAI_EMBEDDINGS_FOLDER_PATH, UPLOAD_FOLDER   



# class SimpleContextProvider(builtins): 
#     def __init__(self) -> None:
#         self.list_csv_path: list[str] = [
#             os.path.join(CSV_STORAGE_FOLDER,path)
#             for path in os.listdir(CSV_STORAGE_FOLDER) 
#         ]
#         self.recent_uploaded_files: list[str] = [] 

LIST_CSV_IN_DB: list[str] = [
            os.path.join(CSV_STORAGE_FOLDER,path)
            for path in os.listdir(CSV_STORAGE_FOLDER) 
]

RECENT_UPLOAD: list[str] = [] 