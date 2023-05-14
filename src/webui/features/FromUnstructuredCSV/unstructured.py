import gradio as gr

DEFAULT_SUMMARY_PORMPT = """[Summary]: [Write a concise summary of the review which is approximately 25-35% of the length, with no paragraphs, and designed so that if you were reading a high volume of these summaries, you would get a good understanding of the review.]
[Sentiment] : [One sentence summarising the sentiment of the review, taking account of the text and the scores].
[Positive Quote]: [Set out one positive direct quote from the review which represents the review well.]
[Negative Quote]: [Set out one negative direct quote, if there is one.]
[Topic Quotes]: [Set out any short, direct quotes on facilitates, location, building management, design, pets or children, and label each quote accordingly.]
[Topics]: [Set out a list of topics, described in a single word, which are covered in the review, with no more than 6. If there are more than 6, then just list the 6 most prevalent.]
"""

DEFAULT_FORMAT_INSTRUCTION = ''' CSV line with new fields created. 
The result must follow this CSV format:
```
id\tsummary\tsentiment\tpositive_quote\tnegative_quote\ttopic_quotes\ttopics
```
REMEMBER, YOU MUST ONLY RETURN CSV TABLE 
'''


# TODO: add handler



# TODO: parse response with formate
def parse_response(response: str) -> str: 
    return 


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
                llm_temperature_slider = gr.Slider(0, 2, step=0.2, value=0.2, label="LLM Temperature (More creative when higher value)")

            with gr.Column(): 
                named_csv_txt_box = gr.Textbox(label="Name the CSV documents")
                file = gr.File(label="Upload CSV Documents")
                uploaded_btn = gr.UploadButton(
                    "Click to upload *.csv file",
                    file_types=[".txt", ".pdf"],
                    file_count="multiple"
                ) 

        output_format_instruct_txt_box = gr.Textbox(label="Generated output based on this format instruction", value=DEFAULT_FORMAT_INSTRUCTION)
        start_btn = gr.Button("!!! Start !!!",variant="primary")

    return block