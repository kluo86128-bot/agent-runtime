
from typing import Any
from pydantic import BaseModel
class ParameterSchema(BaseModel):
    type:str
    description:str
    required:bool
        
    
class ToolSchema(BaseModel):
    name:str
    description:str
    parameters:dict[str,ParameterSchema]
        

    
class ToolResultSchema(BaseModel):
    name:str
    success:bool
    result:Any=None
    error:str

    
    
    