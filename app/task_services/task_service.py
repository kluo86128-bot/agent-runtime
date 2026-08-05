from datetime import datetime
from uuid import uuid4
from app.db.tables import TaskORM
from app.task_shcema.task_schema import TaskCreateRequest,TaskResponse,TaskState   
from app.db.session import SessionLocal
import traceback
from app.log.logger import logger
from app.redis_state.task_state_manage import agent_state_manage_service
from app.redis_queue.task_queue import task_queue
from app.worker.job import execute_agent_task
class TaskService:
    def __init__(self):
        self._tasks:dict[str,TaskResponse]={}
        
    def create_task(self,request:TaskCreateRequest)->TaskResponse:
        task_id=str(uuid4())
        logger.info(
            f"task_service层\n任务创建成功，task_id={task_id}"
        )
        db=SessionLocal()
        
        try:
            db=SessionLocal()
            task=TaskORM(
                id=task_id,
                instruction=request.instruction,
                state=TaskState.runing.value,
                result=None,
                created_at=datetime.utcnow()
            )
            db.add(task)
            db.commit()
            try:
                logger.info(
                    f"任务进入等待队列:task_id={task_id}"
                )
                task_queue.enqueue(
                    execute_agent_task,
                    task_id,
                    request.instruction
                    
                )
                logger.info(
                    f"state:{TaskState.pending.value};task_id={task_id}"
                )
                agent_state_manage_service.update_state(
                    task_id=task_id,
                    state=TaskState.pending.value,
                    step="queued",
                    progress=0
                )

                return self._to_response(task)


            except:
                logger.exception(
                f"create_task失败。traceback:{traceback.format_exc()}"
            )
                task.state=TaskState.failed.value
                task.result=traceback.format_exc()    
                
            db.commit()
            db.refresh(task)
            return self._to_response(task)   
        except:
            db.close()
            logger.exception(
                f"create_task失败。traceback:{traceback.format_exc()}"
            )
            return TaskResponse(
                task_id=task_id,
                instruction=request.instruction,
                state=TaskState.failed.value,                
                result=traceback.format_exc(),
                created_at=datetime.utcnow()
            )


    def _to_response(self,task:TaskORM)->TaskResponse:
        return TaskResponse(
            task_id=task.id,
            instruction=task.instruction,
            result=task.result,
            state=TaskState(task.state),
            created_at=task.created_at
        )
    
    def get_task(self,task_id:str)->TaskResponse|None:
        db=SessionLocal()
        try:
            task=db.query(TaskORM).filter(TaskORM.id==task_id).first()
            if not task:
                return None
            return self._to_response(task)
        except:
            db.close()
task_service=TaskService()
        