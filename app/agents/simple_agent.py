from app.tools.tool_registry import tool_registry
from typing import Any
from app.trace.agent_trace_manage_service import agent_trace_manage_service
from app.redis_state.task_state_manage import agent_state_manage_service
import traceback
import time
from app.log.logger import logger
class SimpleAgent:
    def run(self,task_id:str,instruction:str)->Any:
        logger.info(
            f"agent层\ntask_state:running\ntask_id:{task_id}\ninstruction:{instruction}"
        )
        agent_state_manage_service.update_state(
            task_id,
            state="running",
            step="agent_started",
            progress=0,
        )
        time.sleep(1)
        read_tool=tool_registry.get_tool("read_file")
        write_tool=tool_registry.get_tool("write_file")
        
        try:
            logger.info(
                f"Tool Calling:read_file"
            )
            agent_state_manage_service.update_state(
                task_id,
                state="running",
                step="read_file",
                progress=20
            )
            result=read_tool.execute(path="sample_data/note.txt")
            result=result.model_dump()
            content=str(result.get("result"))
            agent_trace_manage_service.add_trace(
                task_id=task_id,
                step_index=1,
                action="read_file",
                input={"path":"sample_data/note.txt"},
                output={"content_preview":content[:100]},
            )
            agent_state_manage_service.update_state(
                task_id,
                state="running",
                step="summarize",
                progress=60,
            )
            logger.info(f"Tool Calling:summarize")
            summary=self._summary(content)
            agent_trace_manage_service.add_trace(
                task_id=task_id,
                step_index=2,
                action="summarize",
                input={"content_preview":content[:100]},
                output={"summary":summary}
            )
            output_path="output/summary.md"
            agent_state_manage_service.update_state(
                task_id,
                state="running",
                step="write_file",
                progress=80,
            )
            logger.info(f"Tool Calling:writer_file")
            write_result=write_tool.execute(path=output_path,content=summary)
            agent_trace_manage_service.add_trace(task_id=task_id,
                                    step_index=3,
                                    action="write_file",
                                    input={"path":output_path},
                                    output={"summary":summary})
            agent_state_manage_service.update_state(
                task_id,
                state="completed",
                step="finnished",
                progress=100
            )
            return write_result
            
        except Exception as e:
            agent_trace_manage_service.add_trace(
                task_id=task_id,
                step_index=999,
                action="agent_error",
                input={"instruction":instruction},
                output=None,
                error_type=type(e).__name__,
                error_message=str(e),
                error_trace=traceback.format_exc()
            )
            raise 
           
    def _summary(self,content:str)->str:
        lines=[line.strip() for line in content.splitlines() if line.strip()]
        
        if not lines:
            return "No content to summary"
        return "摘要：\n" + "\n".join(f"- {line}" for line in lines[:3])
    
simple_agent=SimpleAgent()