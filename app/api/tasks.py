from fastapi import APIRouter,HTTPException
from app.models.task import TaskCreateRequest,TaskResponse
from app.services.task_service import task_service
from app.services.trace_service import trace_service
from app.models.trace import TraceRecord
from app.services.state_service import state_service
router=APIRouter(prefix="/tasks",tags=["tasks"])

@router.post("",response_model=TaskResponse)
def create_task(request:TaskCreateRequest):
    return task_service.create_task(request)



@router.get("/{task_id}/traces",response_model=list[TraceRecord])
def get_task_trace(task_id:str):
    task=task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    
    return trace_service.get_trace(task_id)


@router.get("/{task_id}",response_model=TaskResponse)
def get_task(task_id:str):
    task=task_service.get_task(task_id)
    
    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    
    return task

@router.get("/{task_id}/state")
def get_task_state(task_id:str):
    
    state=state_service.get_state(task_id)
    
    if state is None:
        raise HTTPException(
            status_code=404,
            detail="Status not found"
        )
        
    return state