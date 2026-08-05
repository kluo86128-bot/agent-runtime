from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel,Field

class TaskState(str,Enum):
    pending="pending"
    runing="runing"
    completed="completed"
    failed="failed"
    
class TaskCreateRequest(BaseModel):
    instruction:str=Field(...,description="The user instrucion for the agent.")
    
class TaskResponse(BaseModel):
    task_id:str
    instruction:str
    state:TaskState
    result:Optional[str]=None
    error_type:str|None=None
    error_message:str|None=None
    error_trace:str|None=None
    created_at:datetime