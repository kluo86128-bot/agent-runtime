from openai import OpenAI
from app.llm.schema import LLMResponse

class LLMClient:
    def __init__(
        self,
        api_key:str,
        base_url:str,
        model:str
    ):
        self.client=OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model=model
        
    def chat(
        self,
        messages:list[dict],
        tools:list[dict]|None=None,
        temperature:float=0.7
    ):
        kwargs={
            "model":self.model,
            "messages":messages,
            "temperature":temperature
        }
        
        if tools:
            kwargs["tools"]=tools
            kwargs["tool_choice"]="auto"
        response=self.client.chat.completions.create(
            **kwargs
        )
        
        return response
