from app.tools.tool_registry import tool_registry
from app.services.trace_service import trace_service
from app.services.state_service import state_service
import traceback
import time
class SimpleAgent:
    def run(self,task_id:str,instruction:str)->str:
        state_service.update_state(
            task_id,
            status="running",
            step="agent_started",
            progress=0,
        )
        time.sleep(1)
        read_tool=tool_registry.get_tool("read_file")
        write_tool=tool_registry.get_tool("write_file")
        
        try:
            state_service.update_state(
                task_id,
                status="running",
                step="read_file",
                progress=20
            )
            content=read_tool.run(path="sample_data/note.txt")
            trace_service.add_trace(
                task_id=task_id,
                step_index=1,
                action="read_file",
                input={"path":"sample_data/note.txt"},
                output={"content_preview":content[:100]},
            )
            state_service.update_state(
                task_id,
                status="running",
                step="summarize",
                progress=60,
            )
            summary=self._summary(content)
            trace_service.add_trace(
                task_id=task_id,
                step_index=2,
                action="summarize",
                input={"content_preview":content[:100]},
                output={"summary":summary}
            )
            output_path="output/summary.md"
            state_service.update_state(
                task_id,
                status="running",
                step="write_file",
                progress=80,
            )
            write_result=write_tool.run(path=output_path,content=summary)
            trace_service.add_trace(task_id=task_id,
                                    step_index=3,
                                    action="write_file",
                                    input={"path":output_path},
                                    output={"summary":summary})
            state_service.update_state(
                task_id,
                status="completed",
                step="finnished",
                progress=100
            )
            return write_result
            
        except Exception as e:
            print(2)
            trace_service.add_trace(
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