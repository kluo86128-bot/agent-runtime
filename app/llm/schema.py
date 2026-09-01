from typing import Any
from pydantic import BaseModel

class LLMResponse(BaseModel):
    content:str
    model:str
    usage:dict[str,Any]|None=None
    