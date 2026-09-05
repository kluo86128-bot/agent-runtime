import json

from app.llm.llm_service import llm_service
from app.tools.tool_registry import  tool_registry
from app.log.logger import logger
import traceback
from app.trace.agent_trace_manage_service import agent_trace_manage_service
from app.task_schema.task_schema import TaskState
from app.redis_state.task_state_manage import agent_state_manage_service
from app.task_schema.task_schema import AgentStep
import time
class FunctionCallAgent:
    def __init__(self):
        self.llm_service=llm_service
        self.tool_registry=tool_registry
        
    def run(self,max_steps:int,instruction:str,task_id=""):
        if max_steps<1:
            raise RuntimeError("max_steps必须大于等于1")
        tool_schemas=(
            self.tool_registry.get_openai_tool_schemas()
        )
        
        logger.info(f"工具箱:{tool_schemas}\n")
        messages=[
            {
                "role":"system",
                "content":(
                    "你是一个能够使用工具完成任务的Agent。"
                    "请根据用户任务判断是否需要调用工具。"
                )
            },
            {
                "role":"user",
                "content":instruction
            }
        ]
        
        for step in range(1,max_steps+1):
            llm_request=None
            message=None
            tool_call_message=None
            tool_results=[]
            try:
            
                time.sleep(5)
                agent_state_manage_service.update_state(
                    task_id=task_id,
                    state=TaskState.runing.value,
                    step=AgentStep.model_request.value,
                    model_step=step,
                    max_steps=max_steps,
                )
                response=self.llm_service.chat(
                    messages=messages,
                    tools=tool_schemas,
                    temperature=0
                )
                llm_request={
                    "message_cnt":len(messages),
                    "tools":self.tool_registry.list_tools()
                }
                message=response.choices[0].message
                
                print("\n============LLM Response========")
                logger.info(message)
                
                if not message.tool_calls:
                    print("\n模型没有选择工具")
                    if not message.content or not message.content.strip():
                        raise ValueError("模型未返回有效答案")
                    agent_trace_manage_service.add_trace(
                        task_id=task_id,
                        model_step=step,
                        llm_request=llm_request,
                        llm_response=message.content,
                        final_answer=message.content
                    )
                    return{
                        "type":"answer",
                        "steps":step,
                        "state":TaskState.completed.value,
                        "content":message.content
                    }
    

                tool_call_message = {
                    "calls": [
                        {
                            "id": call.id,
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        }
                        for call in message.tool_calls
                    ]
                }                
                    
                agent_state_manage_service.update_state(
                    task_id=task_id,
                    state=TaskState.runing.value,
                    step=AgentStep.tool_calling.value,
                    tool_name=tool_call_message,
                    model_step=step,
                    max_steps=max_steps,
                )
                messages.append(message.model_dump(exclude_none=True))
                for tool_call in message.tool_calls:
                    tool_name=tool_call.function.name
                    arguments=json.loads(
                        tool_call.function.arguments
                    )
                    print("\n============Function Call==============")
                    print(f"tool_name:{tool_name}")
                    print(
                        "arguments:",json.dumps(arguments,indent=2,ensure_ascii=False)
                    )
                    tool=self.tool_registry.get_tool(tool_name)
                    time.sleep(5)                
                    agent_state_manage_service.update_state(
                        task_id=task_id,
                        state=TaskState.runing.value,
                        step=AgentStep.tool_execute.value,
                        tool_name=tool_call_message,
                        model_step=step,
                        max_steps=max_steps,                )                
                    tool_result=tool.execute(**arguments)
                    tool_results.append(tool_result.model_dump())
                    if tool_result.success==False:
                        raise RuntimeError(f"\nRuntimeError in {tool_name} calling:{tool_result.error}")
                    messages.append({
                        "role":"tool",
                        "tool_call_id":tool_call.id,
                        "content":tool_result.model_dump_json()
                        })

                    



                if step == max_steps:
                    agent_trace_manage_service.add_trace(
                        task_id=task_id,
                        model_step=step,
                        llm_request=llm_request,
                        llm_response=message.content,
                        tool_call=tool_call_message,
                        tool_result=tool_results,
                        error_trace="模型轮数已达上限"
                    )

                    logger.info(f"模型轮数已达上限")
                    return {
                        "state": TaskState.stopped.value,
                        "reason": "max_steps",
                        "steps": step,
                        "last_tool_results": tool_results,
                    }
                
                agent_trace_manage_service.add_trace(
                    task_id=task_id,
                    model_step=step,
                    llm_request=llm_request,
                    llm_response=message.content,
                    tool_call=tool_call_message,
                    tool_result=tool_results,
                )
                
            except Exception as e:
                agent_trace_manage_service.add_trace(
                    task_id=task_id,
                    model_step=step,
                    llm_request=llm_request,
                    llm_response=(
                        message.content if message is not None else None
                    ),
                    tool_call=tool_call_message,
                    tool_result=tool_results,
                    error_trace=traceback.format_exc()
                    
                )
                raise
            
function_call_agent=FunctionCallAgent()