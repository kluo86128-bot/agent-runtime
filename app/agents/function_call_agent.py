import json

from app.llm.llm_service import llm_service
from app.tools.tool_registry import  tool_registry
from app.log.logger import logger

class FunctionCallAgent:
    def __init__(self):
        self.llm_service=llm_service
        self.tool_registry=tool_registry
        
    def run(self,instruction:str,task_id=""):
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
        return {
            "type":"tool_call",
            "tool_name":tool_name,
            "arguments":arguments
        }
function_call_agent=FunctionCallAgent()