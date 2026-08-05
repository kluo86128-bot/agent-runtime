from fastapi import APIRouter
from app.tools.tool_registry import tool_registry
router=APIRouter(prefix="/tools",tags=["tools"])

@router.get("")
def list_tools():
    return tool_registry.list_tools()

@router.post("/read-file")
def read_file(path:str):
    tool=tool_registry.get_tool("read_file")
    return {"content":tool.run(path=path)}
