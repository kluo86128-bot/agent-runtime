
import traceback

from app.agents.simple_agent import simple_agent
from app.db.models import TaskORM
from app.db.session import SessionLocal
from app.models.task import TaskStatus
from app.services.state_service import state_service

def execute_agent_task(task_id:str,instruction:str)->None:
    db=SessionLocal()

    try:
        task=(
            db.query(TaskORM).
            filter(TaskORM.id==task_id)
            .first()
        )
        if task is None:
            raise ValueError(f"Task not found:{task_id}")
        
        task.status=TaskStatus.runing.value
        db.commit()
        
        state_service.update_state(
            task_id=task_id,
            status=TaskStatus.runing.value,
            step="worker_started",
            progress=0
        )
        result=simple_agent.run(
            task_id=task_id,
            instruction=instruction
        )
        
        task.status=TaskStatus.completed.value
        task.result=result
        db.commit()
        
        state_service.update_state(
            task_id=task_id,
            status=TaskStatus.completed.value,
            step="finished",
            progress=100
        )
        
    except Exception:
            error_trace=traceback.format_exc()
            db.rollback()
            task=(
                db.query(TaskORM)
                .filter(TaskORM.id==task_id)
                .first()
            )
            
            if task is not None:
                task.status=TaskStatus.failed.value
                task.result=error_trace
                db.commit()
            state_service.update_state(
                task_id=task_id,
                status=TaskStatus.failed.value,
                step="failed",
                progress=100,
            )
            
            raise
        
    finally:
        db.close()