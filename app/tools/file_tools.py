from pathlib import Path
from app.tools.base_tool import BaseTool
from app.tools.schema import ParameterSchema
from app.tools.schema import ToolSchema
from app.tools.schema import ToolResultSchema
import traceback
class ReadFileTool(BaseTool):
    name="read_file"
    description="read text from a file"
    parameters={
        "path":ParameterSchema(type="string",
                               description="文件路径",
                               required=True)
        
    }
    schema=ToolSchema(name=name,description=description,parameters=parameters)
    
    def execute(self,path:str)->ToolResultSchema:
        try:
            file_path=Path(path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"file not found:{path}")
            
            text=file_path.read_text(encoding="utf-8")
            return ToolResultSchema(
                name=self.name,
                success=True,
                result=text,
                error=""
                
            )
            
        except Exception as e:
                return ToolResultSchema(
                    name=self.name,
                    success=False,
                    result="",
                    error=traceback.format_exc()
                                                                        
                )
                

class WriteFileTool(BaseTool):
    name="write_file"
    description="write text content to a file"
    parameters={
        "path":ParameterSchema(type="string",
                               description="文件路径",
                               required=True),
        "content":ParameterSchema(type="string",
                                  description="文件内容",
                                  required=True)
        
    }    
    schema=ToolSchema(name=name,description=description,parameters=parameters)
    
    def execute(self,path:str,content:str)->ToolResultSchema:
        try:
            file_path=Path(path)
            file_path.parent.mkdir(parents=True,exist_ok=True)
            file_path.write_text(content,encoding="utf-8")
            return ToolResultSchema(
                name=self.name,
                success=True,
                result=f"已成功写入文件{path}:{content}",
                error=""
            )
        except Exception as e:
            return ToolResultSchema(
                name=self.name,
                success=False,
                result="",
                error=traceback.format_exc()
            )
    
class ListFilesTool(BaseTool):
    name="list_files"
    description="List files in a directory"
    parameters={
        "path":ParameterSchema(type="string",
                               description="文件目录",
                               required=True)
    }
    schema=ToolSchema(name=name,description=description,parameters=parameters)
    def execute(self,path:str)->list[str]:
        try:
            dir_path=Path(path)   
            files=[str(p) for p in dir_path.iterdir()]
            return ToolResultSchema(
                name=self.name,
                success=True,
                result=files,
                error=""
            )
        except Exception as e:
            return ToolResultSchema(
                name=self.name,
                success=False,
                result="",
                error=traceback.format_exc()
            )
