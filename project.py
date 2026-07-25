import os
from typing import TypedDict

# let's create the state 1st

class pipelinestate(TypedDict):
    raw_input : str
    edited_text : str
    script_text : str
    final_output : str
    

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

# let's create the Node

def editor_node(state : pipelinestate) -> dict:
    """Stage 1 : Cleans up grammar, remove types, and refines the tone"""
    
    prompt = (
        "You are an expert editor. Clean up the grammar, fix any typos, "
        "and refine the tone of the following text while keeping its core message intact.\n\n"
        f"Text:{state['raw_input']}"
    )
    
    response = llm.invoke(prompt)
    
    return {"edited_text" : response.content.strip()}


def scriptwriter_node(state: pipelinestate) -> dict:
    """Stage 2 : Converts edited text into an engaging, natural script format"""
    print("Stage 2 : Executing ScriptWriter Node")
    
    prompt = (
        "You are a professional scriptwriter. Take the following polished text "
        "and transform it into a clear, engaging, and well-paced spoken script suitable for a video or audio production.\n\n"
        f"Text:{state['edited_text']}"
    )
    
    response = llm.invoke(prompt)
    
    return {"script_text": response.content.strip()}



def translator_node(state: pipelinestate) -> dict:
    """Stage 3 : Translates the script into natural Nepanglish (Romanized Nepali)"""
    print("Stage 3 : Executing Translator Node")
    
    prompt = (
        "You are an expert translator specializing in informal spoken communication. "
        "Translate the following script into natural, conversational Nepanglish "
        "(Nepali written in the Roman/English alphabet). Keep the tone friendly, "
        "engaging, and easy to speak out loud.\n\n"
        f"Text:{state['script_text']}"
    )
    
    response = llm.invoke(prompt)
    
    return {"final_output": response.content.strip()}



# now your state and nodes are ready & now it's time to create the graph
#  & for creating the graph you  have to connect these nodes & for that you've to use the edges
# edges are very important to create the workflows

from langgraph.graph import StateGraph, START, END

# create the graph 
graph = StateGraph(pipelinestate)

# add the nodes in our graph

graph.add_node("editor",editor_node)
graph.add_node("scriptwriter",scriptwriter_node)
graph.add_node("translator",translator_node)



# Add edges (sequential) - one after another

graph.add_edge(START, "editor") 
graph.add_edge("editor", "scriptwriter")
graph.add_edge("scriptwriter", "translator")
graph.add_edge("translator", END)


# compile the Graph
app = graph.compile() 

result = app.invoke({
    "raw_input" : "AI Agents are the future of tech. They can think plan & act on their own. Langgraph helps you build these agents with peoper control & memory"
})

# Final Output 
print("Your result are :- \n\n")
print(result['final_output'])