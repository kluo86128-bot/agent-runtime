import json

from app.llm.llm_service import llm_service
from app.tools.tool_registry import  tool_registry
from app.log.logger import logger

class FunctionCallAgent:
    def __init__(self):
        self.llm_service=llm_service
        self.tool_registry=tool_registry
        
    def run(self,max_steps:int,instruction:str,task_id=""):
        tool_schemas=(
            self.tool_registry.get_openai_tool_shcemas()
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
            
            response=self.llm_service.chat(
                messages=messages,
                tools=tool_schemas,
                temperature=0
            )
            
            message=response.choices[0].message
            
            print("\n============LLM Response========")
            logger.info(message)
            
            if not message.tool_calls:
                print("\n模型没有选择工具")
                return{
                    "type":"answer",
                    "content":message.content
                }
            
            if step == max_steps:
                raise RuntimeError("模型轮次已达上限，不在执行工具")
            
            
            if len(message.tool_calls)>1:
                raise RuntimeError("\n当前版本支支持单次工具调用")
            tool_call=message.tool_calls[0]
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
            tool_result=tool.execute(**arguments)
            if tool_result.success==False:
                raise RuntimeError(f"\nRuntimeError in {tool_name} calling:{tool_result.error}")

            messages.append(message.model_dump(exclude_none=True))
            
            messages.append({
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":tool_result.model_dump_json()
            })
            
function_call_agent=FunctionCallAgent()