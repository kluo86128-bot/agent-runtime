from fastapi import APIRouter,HTTPException
from app.redis_state.task_state_manage import agent_state_manage_service
router=APIRouter(prefix="/task_state",tags=["task_state"])
@router.get("/{task_id}/state")
def get_task_schema(task_id:str):
    
    state=agent_state_manage_service.get_state(task_id)
    
    if state is None:
        raise HTTPException(
            state_code=404,
            detail="state not found"
        )
        
    return state