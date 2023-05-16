import os 
import gradio as gr 
import pandas as pd 
from src.constants import UPLOAD_FOLDER
from src.utils.logger import get_logger 
from src.webui.ContextProvider.SimpleContext import LIST_CSV_IN_DB 


logger = get_logger()


def refresh_btn_handler() -> gr.Dropdown:
    global LIST_CSV_IN_DB  # NOTE: dirty way to do similar to gr.State()
    LIST_CSV_IN_DB = os.listdir(UPLOAD_FOLDER)
    logger.info(f"Refresh list csv {LIST_CSV_IN_DB}")
    return gr.Dropdown.update(choices=LIST_CSV_IN_DB)


def change_csv_handler(csv_filepath: str) -> gr.Dataframe: 
    df = pd.read_csv(csv_filepath,sep="\t")
    logger.info(f"Change to dataframe {csv_filepath}")
    return gr.Dataframe.update(value = df), gr.File.update(value=csv_filepath) 


def csv_viewer() -> gr.Blocks: 
    global LIST_CSV_IN_DB 

    block = gr.Blocks() 
    with block: 
        with gr.Row(): 
            file = gr.File(label="Output CSV Download")
        with gr.Row(): 
            csv_dropdown = gr.Dropdown(
                choices=LIST_CSV_IN_DB, 
                label="Select CSV to view", 
                value=LIST_CSV_IN_DB[0] if LIST_CSV_IN_DB \
                                        else None # TODO: pass csv list files here
            )
            csv_refresh_btn = gr.Button("⟳ Refresh Collections").style(full_width=False)  


        df_viewer = gr.Dataframe(None, label="Default pricing list table (for comparision)")

        # NOTE: event handler
        csv_refresh_btn.click(
            fn=refresh_btn_handler, 
            outputs=csv_dropdown
        )

        csv_dropdown.change(change_csv_handler, 
            inputs=csv_dropdown, 
            outputs=[df_viewer,file]
        ) 


    return block    
