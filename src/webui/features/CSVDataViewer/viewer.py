import gradio as gr 
import pandas as pd 

# TODO: add handler



def csv_viewer() -> gr.Blocks: 
    block = gr.Blocks() 
    with block: 
        with gr.Row(): 
            csv_dropdown = gr.Dropdown(
                value=None, 
                label="Select CSV to view", 
                choices=[] # TODO: pass csv list files here
            )
            csv_refresh_btn = gr.Button("⟳ Refresh Collections").style(full_width=False)  
            download_btn = gr.Button("Download CSV").style(full_width=False)   
        

        if csv_dropdown.value != None:  
            df = pd.read_csv("./comma_pricing_list.csv")
            gr.Dataframe(df, label="Default pricing list table (for comparision)")

    return block    
