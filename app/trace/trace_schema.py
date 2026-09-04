from datetime import datetime
from typing import Optional,Any
from pydantic import BaseModel,Field
from app.tools.schema import ToolResultSchema
class TraceRecord(BaseModel):
    trace_id:str
    task_id:str
    model_step:Optional[int] = None
    llm_request:dict[str,Any]|None=None
    llm_response:str|None=None
    tool_call:dict[str,Any]|None=None
    tool_result:ToolResultSchema|None=None
    final_answer:Any
    error_trace:str|None=None
    created_at:datetime=Field(default_factory=datetime.utcnow)
