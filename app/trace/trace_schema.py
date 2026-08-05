from datetime import datetime
from typing import Optional,Any
from pydantic import BaseModel,Field

class TraceRecord(BaseModel):
    trace_id:str
    task_id:str
    step_index:int
    action:str
    input:Optional[Any]=None
    output:Optional[Any]=None
    error_type:str|None=None
    error_message:str|None=None
    error_trace:str|None=None
    created_at:datetime=Field(default_factory=datetime.utcnow)