import pandas as pd 
import gradio as gr

from src.webui.features.FromUnstructuredCSV.prompt import _get_prompt, DEFAULT_SYSTEM_PROMPT 
from src.utils.df_utils import string_to_df 

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, BaseMessage, LLMResult


def _batch_llm_predict(list_prompt: list[str], temperature: float = 0.0) -> list[str]: 
    def _from_llmresult_to_str(llm_result: LLMResult) -> list[str]: 
        result: str = []
        for res in llm_result.generations: 
            result.append(res[0].text)
        return result 

    chat = ChatOpenAI(temperature=temperature)

    openai_messages: list[list[BaseMessage]] = []
    for prompt in list_prompt: 
        openai_messages.append([
            SystemMessage(content=DEFAULT_SYSTEM_PROMPT), 
            HumanMessage(content=prompt)
        ]) 
    response_messages: LLMResult = chat.generate(openai_messages)
    response: list[str] = _from_llmresult_to_str(response_messages)
    return response


# NOTE: unstable 
def batch_transform(
    batch_size: int = 5, 
    filepath: str = None,  
    llm_temperature: float = 0.0,
    custom_summary_prompt: str = None, 
    custom_format_instruct: str = None, 
    progress = gr.Progress() 
) -> pd.DataFrame: 
    with open(filepath,"r",encoding="utf-8") as f: 
        data = f.readlines()
    header = data[0]
    data = data[1:]

    df = pd.DataFrame()
    idx = 0 
    while idx < len(data): 
        batch: list[str] = data[idx:idx+batch_size]
        list_prompt: list[str] = [ 
        _get_prompt(context_prompt=header + "\n" + val, 
                custom_format_instruct=custom_format_instruct, 
                custom_summary_prompt=custom_summary_prompt)
            for val in batch
        ]
        response: list[str] = _batch_llm_predict(list_prompt=list_prompt, temperature=llm_temperature)

        list_df: list[pd.DataFrame] = []
        for r in response: 
            try: 
                _r: pd.DataFrame = string_to_df(r)
                list_df.append(_r) 
            except ValueError: 
                continue

        _df = pd.concat(list_df)
        df = pd.concat([df,_df])

        idx += batch_size

    return df 


##########################################################

def _llm_predict(prompt: str, temperature: float = 0.0) -> str: 
    chat = ChatOpenAI(temperature=temperature)
    response = chat([
        SystemMessage(content=DEFAULT_SYSTEM_PROMPT), 
        HumanMessage(content=prompt)
    ])
    return response.content 


def transform(
    filepath: str = None, 
    llm_temperature: float = 0.0,
    custom_summary_prompt: str = None, 
    custom_format_instruct: str = None, 
    progress = gr.Progress() 
) -> pd.DataFrame: 
    with open(filepath,"r",encoding="utf-8") as f: 
        data: list[str] = f.readlines()
    header = data[0]
    data = data[1:]

    df = pd.DataFrame()
    progress(0, "Starting...")
    for row in progress.tqdm(data): 
        input = header + "\n" + row
        prompt = _get_prompt(context_prompt=input, 
                    custom_format_instruct=custom_format_instruct, 
                    custom_summary_prompt=custom_summary_prompt)
        response = _llm_predict(prompt=prompt, temperature=llm_temperature)
        try: 
            _df = string_to_df(value=response) 
        except ValueError: 
            continue

        df = pd.concat([df,_df])
    return df 