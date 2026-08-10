from abc import ABC,abstractmethod
from typing import Any
from app.tools.schema import ParameterSchema
from app.tools.schema import ToolSchema
from app.tools.schema import ToolResultSchema
class BaseTool(ABC):
    name:str
    description:str
    parameters:dict[str,ParameterSchema]
    schema:ToolSchema
    @abstractmethod
    def execute(self,**kwargs)->ToolResultSchema:
        pass
    
    
