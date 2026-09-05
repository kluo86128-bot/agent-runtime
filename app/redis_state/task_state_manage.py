import json
from typing import Any

from app.redis_base.redis_client import redis_client

class AgentStateManageService:
    PREFIX="agent:task"
    
    def _key(self,task_id:str):
        return f"{self.PREFIX}:{task_id}:state"
    
    def update_state(
        self,
        task_id:str,
        state:str|None=None,
        step:str|None=None,
        tool_name:dict[str,Any]|None=None,
        model_step:int|None=None,
        max_steps:int|None=None,
        reason:str|None=None
    ):
        state={
            "state":state,
            "step":step,
            "tool_name":tool_name,
            "model_step":model_step,
            "max_steps":max_steps,
            "reason":reason
        }
        redis_client.set(
            self._key(task_id),
            json.dumps(state,ensure_ascii=False),
        )
        
    def get_state(self,task_id:str):
        data=redis_client.get(
            self._key(task_id)
        )
        
        if data is None:
            return None
        return json.loads(data)
    
    
    def delete_state(self,task_id:str):
        redis_client.delete(
            self._key(task_id)
        )
        
agent_state_manage_service=AgentStateManageService()