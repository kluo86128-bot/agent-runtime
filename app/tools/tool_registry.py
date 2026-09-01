from app.tools.base_tool import BaseTool
from app.tools.file_tools import ReadFileTool,WriteFileTool,ListFilesTool
from app.tools.schema import ToolSchema
class ToolRegistry:
    def __init__(self):
        self.__tools:dict[str,BaseTool]={}
        
    def register(self,tool:BaseTool):
        self.__tools[tool.name]=tool
        
    def get_tool(self,name:str)->BaseTool:
        if name not in self.__tools:
            return ValueError(f"Tool not found:{name}")
        return self.__tools[name]
    
    def get_tool_schema(self)->list[dict]:
        schema_list=[]
        for tool in self.__tools.values():
            schema_list.append(tool.schema.model_dump())
        return schema_list
        
    def list_tools(self)->list[dict[str,str]]:
        return [
            {
                "name":tool.name,
                "description":tool.description
            }
            for tool in self.__tools.values()
        ]
        
    def get_openai_tool_shcemas(self)->list[dict]:
        tools=[]
        
        for tool in self.__tools.values():
            properties={}
            required=[]
            
            for param_name,param_schema in tool.parameters.items():
                properties[param_name]={
                    "type":param_schema.type,
                    "description":param_schema.description
                }
                
                if param_schema.required:
                    required.append(param_name)
                
            tool_schema={
                "type":"function",
                "function":{
                    "name":tool.name,
                    "description":tool.description,
                    "parameters":{
                        "type":"object",
                        "properties":properties,
                        "required":required
                    }
                }
            }
            tools.append(tool_schema)
                
            
        return tools
            
        
        
tool_registry=ToolRegistry()
tool_registry.register(ReadFileTool())
tool_registry.register(WriteFileTool())
tool_registry.register(ListFilesTool())
    