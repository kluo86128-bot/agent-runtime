from fastapi import APIRouter,HTTPException
from app.task_shcema.task_schema import TaskCreateRequest,TaskResponse
from app.task_services.task_service import task_service
from app.log.logger import logger
router=APIRouter(prefix="/tasks",tags=["tasks"])

@router.post("",response_model=TaskResponse)
def create_task(request:TaskCreateRequest):
    logger.info(
        f"请求进入：create_task"
    )
    return task_service.create_task(request)


@router.get("/{task_id}",response_model=TaskResponse)
def get_task(task_id:str):
    task=task_service.get_task(task_id)
    logger.info(
        f"请求进入：get_task|task_id={task_id}"
    )
    if task is None:
        logger.info(
            f"task_id={task_id}:Task not found"
        )
        raise HTTPException(status_code=404,detail="Task not found")
    
    return task

