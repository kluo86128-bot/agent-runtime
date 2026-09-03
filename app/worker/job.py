
import traceback
import time
from app.agents.simple_agent import simple_agent
from app.agents.function_call_agent import function_call_agent
from app.db.tables import TaskORM
from app.db.session import SessionLocal
from app.task_shcema.task_schema import TaskState
from app.redis_state.task_state_manage import agent_state_manage_service
from app.log.logger import logger
import json
from app.llm.config import get_required_env
from dotenv import load_dotenv
load_dotenv()
def execute_agent_task(task_id:str,instruction:str)->None:

    try:
        with SessionLocal() as db:
            logger.info(
                f"create_task\nworker层\ntask_state:running\ntask_id:{task_id}\ninstruction:{instruction}"
            )
            task=(
                db.query(TaskORM).
                filter(TaskORM.id==task_id)
                .first()
            )
            if task is None:
                raise ValueError(f"Task not found:{task_id}")
            
            task.state=TaskState.runing.value
            db.commit()
        
        agent_state_manage_service.update_state(
            task_id=task_id,
            state=TaskState.runing.value,
            step="worker_started",
            progress=0
        )

        result=function_call_agent.run(
            task_id=task_id,
            max_steps=int(get_required_env("MAX_STEPS")),
            instruction=instruction
        )
        with SessionLocal() as db:
            task=(db.query(TaskORM).
                  filter(TaskORM.id==task_id)
                  .first())
            if task is None:
                raise ValueError(f"Task not found:{task_id}")
            task.state=TaskState.completed.value
            result=json.dumps(result,ensure_ascii=False)
            task.result=result
            db.commit()
        
        agent_state_manage_service.update_state(
            task_id=task_id,
            state=TaskState.completed.value,
            step="finished",
            progress=100
        )
        
    except Exception:
        with SessionLocal() as db:
            logger.exception(f"create_task\nworker层\n任务执行时出现异常")
            error_trace=traceback.format_exc()
            db.rollback()
            task=(
                db.query(TaskORM)
                .filter(TaskORM.id==task_id)
                .first()
            )
            
            if task is not None:
                task.state=TaskState.failed.value
                task.result=error_trace
                db.commit()
            agent_state_manage_service.update_state(
                task_id=task_id,
                state=TaskState.failed.value,
                step="failed",
                progress=100,
            )
            
            raise