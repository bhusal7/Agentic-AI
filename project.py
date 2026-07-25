import os
from typing import TypedDict

# let's create the state 1st

class pipelinestate(TypedDict):
    raw_input : str
    edited_text : str
    script_text : str
    final_ouput : str
    

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

# let's create the Node

def editor_node(state : pipelinestate) -> dict:
    
