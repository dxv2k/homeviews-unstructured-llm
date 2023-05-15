import os 
import shutil
import gradio as gr

from src.constants import UPLOAD_FOLDER
from src.utils.df_utils import save_df_to_csv
from src.utils.file_helper import get_filename
from src.utils.logger import get_logger
from src.webui.features.FromUnstructuredCSV.prompt import DEFAULT_FORMAT_INSTRUCTION, DEFAULT_SUMMARY_PORMPT
from src.webui.features.FromUnstructuredCSV.transform import transform 
import src.webui.ContextProvider.SimpleContext # stored global variables

logger = get_logger()

def change_llm_temperature_handler(temperature: float) -> gr.Slider: 
    logger.info(f"Change LLM temperature to {temperature}")
    return gr.Slider.update(value=temperature)


def upload_handler(files) -> list[str]: 
    try: 
        file_paths = [file.name for file in files]
        
        # loop over all files in the source directory
        uploads_filepath = []
        for path in file_paths:
            filename = get_filename(path)
            destination_path = os.path.join(UPLOAD_FOLDER, filename)

            # copy file from source to destination
            shutil.copy(path, destination_path)
            uploads_filepath.append(destination_path)

        global RECENT_UPLOAD 
        RECENT_UPLOAD = uploads_filepath 
        logger.info(f"Recent uploaded files: {RECENT_UPLOAD}")
        return uploads_filepath
    except Exception as e: 
        logger.error(f"{e}")
        raise gr.Error("Error encounter, please contact the developer...")


def start_transform_handler(
    user_summarize_prompt,# str 
    user_format_instruct, # str 
    output_csv_name,# str 
    llm_temperature,  # float 
    progress = gr.Progress()
) -> str: 
    try: 
        global RECENT_UPLOAD 

        logger.info(f"Starting to transform with file {RECENT_UPLOAD}, temperature: {llm_temperature}")
        df = transform(
            filepath=RECENT_UPLOAD[0], 
            llm_temperature=llm_temperature, 
            custom_summary_prompt=user_summarize_prompt, 
            custom_format_instruct=user_format_instruct, 
            progress=progress
        )  

        saved_path = save_df_to_csv(df=df, filename=output_csv_name)
        logger.info(f"Transform complete, saved at {saved_path}")
        return "!!! DONE !!!"

    except Exception as e: 
        logger.error(f"{e}")
        raise gr.Error("Error encounter, please contact the developer...")



def unstructured() -> gr.Blocks: 
    ''' 
    args: 
        None 
    return: 
        gr.Blocks
    '''

    block = gr.Blocks() 
    with block: 
        with gr.Row(): 
            with gr.Column(): 
                summarization_txt_box = gr.Textbox(label="Apply each summarization prompt for every row in the dataframe",
                                        value=DEFAULT_SUMMARY_PORMPT,
                                        lines=15)
                llm_temperature_slider = gr.Slider(0, 2, step=0.1, value=0.0, label="LLM Temperature (Not recommend higher value)")

            with gr.Column(): 
                named_csv_txt_box = gr.Textbox(label="Name output CSV file")
                file = gr.File(label="Upload CSV Documents")
                upload_btn = gr.UploadButton(
                    "Click to upload *.csv file",
                    file_types=[".csv"],
                    file_count="multiple"
                ) 

        output_format_instruct_txt_box = gr.Textbox(label="Generated output based on this format instruction", value=DEFAULT_FORMAT_INSTRUCTION)
        
        # NOTE: start transform handler
        with gr.Row(): 
            start_btn = gr.Button("!!! Start !!!",variant="primary")
            # stop_btn = gr.Button("STOP", variant="stop").style(full_width=True)
        
        # NOTE: event handler section
        upload_btn.upload(upload_handler, upload_btn, file)

        start_btn.click(fn=start_transform_handler, 
                        inputs=[summarization_txt_box, output_format_instruct_txt_box, named_csv_txt_box, llm_temperature_slider], 
                        outputs=named_csv_txt_box)

        llm_temperature_slider.change(
            fn=change_llm_temperature_handler, 
            inputs=llm_temperature_slider, 
            outputs=llm_temperature_slider
        )
        # TODO: how dafuk to implement interrupt button ?

    return block