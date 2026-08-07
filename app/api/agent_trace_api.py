from fastapi import APIRouter,HTTPException
from app.task_services.task_service import task_service
from app.trace.agent_trace_manage_service import agent_trace_manage_service
from app.trace.trace_schema import TraceRecord
router=APIRouter(prefix="/agent_trace",tags=["agent_trace"])
@router.get("/{task_id}/traces",response_model=list[TraceRecord])
def get_task_trace(task_id:str):
    task=task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    
    return agent_trace_manage_service.get_trace(task_id)
