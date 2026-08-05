from pathlib import Path
from app.tools.base import BaseTool

class ReadFileTool(BaseTool):
    name="read_file"
    description="read text from a file"
    
    def run(self,path:str):
        file_path=Path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"file not found:{path}")
        
        return file_path.read_text(encoding="utf-8")
    

class WriteFileTool(BaseTool):
    name="write_file"
    description="write text content to a file"
    
    def run(self,path:str,content:str):
        file_path=Path(path)
        file_path.parent.mkdir(parents=True,exist_ok=True)
        file_path.write_text(content,encoding="utf-8")
        return f"file written sucessfully:{path}"
    
    
class ListFilesTool(BaseTool):
    name="list_files"
    description="List files in a directory"
    
    def run(self,path:str)->list[str]:
        dir_path=Path(path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"file not found error:{path}")
        
        return [str(p) for p in dir_path.iterdir()]
    
