from datetime import datetime
from uuid import uuid4
from app.models.task import TaskCreateRequest,TaskResponse ,TaskStatus
from app.db.models import TaskORM
from app.db.session import SessionLocal
import traceback
from app.services.state_service import state_service
from app.queue.task_queue import task_queue
from app.jobs.agent_job import execute_agent_task
class TaskService:
    def __init__(self):
        self._tasks:dict[str,TaskResponse]={}
        
    def create_task(self,request:TaskCreateRequest)->TaskResponse:
        task_id=str(uuid4())
        db=SessionLocal()
        
        try:
            db=SessionLocal()
            task=TaskORM(
                id=task_id,
                instruction=request.instruction,
                status=TaskStatus.runing.value,
                result=None,
                created_at=datetime.utcnow()
            )
            db.add(task)
            db.commit()
            try:
                task_queue.enqueue(
                    execute_agent_task,
                    task_id,
                    request.instruction
                    
                )
                state_service.update_state(
                    task_id=task_id,
                    status=TaskStatus.pending.value,
                    step="queued",
                    progress=0
                )
                return self._to_response(task)


            except:
                task.status=TaskStatus.failed.value
                task.result=traceback.format_exc()    
                
            db.commit()
            db.refresh(task)
            return self._to_response(task)   
        except:
            db.close()
            return TaskResponse(
                task_id=task_id,
                instruction=request.instruction,
                status=TaskStatus.failed.value,                
                result=traceback.format_exc(),
                created_at=datetime.utcnow()
            )


    def _to_response(self,task:TaskORM)->TaskResponse:
        return TaskResponse(
            task_id=task.id,
            instruction=task.instruction,
            result=task.result,
            status=TaskStatus(task.status),
            created_at=task.created_at
        )
    
    def get_task(self,task_id:str)->TaskResponse|None:
        db=SessionLocal()
        try:
            task=db.query(TaskORM).filter(TaskORM.id==task_id).first()
            if not task:
                print("None")
                return None
            print("None")
            return self._to_response(task)
        except:
            db.close()
task_service=TaskService()
        