# so now we are creating a graph 
# and the 1st thing you create is a state

import os

# 1. typed DICT (Most commom state)

from typing import TypedDict

class State(TypedDict):
    topic : str
    summary : str
    score : int
    
    
    
# 2. Pydantic Approach
# It's good at data validation and data validation

from pydantic import BaseModel, field_validator

class State(BaseModel):
    topic : str
    summary : str = ""
    score : int
    
    @field_validator
    def score_positive(cls,v):  # 'cls' target the State & 'v' target the Score which we will get
        if v < 0:
            raise ValueError("score must be positive")
        
        
        
# 3. python dataclasses
# standard python dataclasses but it's used very rarely

from dataclasses import dataclass, field

@dataclass
class State:
    topic : str = ""
    summary : str = ""
    messages : list = field(default_factory=list)
    
    
# 4. MessagesState

from langgraph.graph import MessagesState

class State(MessagesState):
    # message field is already included with add_messages reducer
    # just add your extra fields
    user_name : str
    language : str
    