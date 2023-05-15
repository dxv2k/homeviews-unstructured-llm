import gradio as gr

from src.webui.features.CSVDataViewer.ui import csv_viewer 
from src.webui.features.FromUnstructuredCSV.ui import unstructured


def web() -> gr.Blocks: 
    block = gr.Blocks(css=".gradio-container {background-color: lightgray}")
    with block:     
        with gr.Tab("LLM Unstructured to Structured"): 
            unstructured()            

        with gr.Tab("CSV Viewer"): 
            csv_viewer() 

    return block