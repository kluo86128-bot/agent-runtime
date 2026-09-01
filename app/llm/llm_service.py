from app.llm.llm_client import LLMClient
from app.llm.schema import LLMResponse
from app.llm.config import LLM_CONFIG
class LLMService:
    def __init__(
        self,
        client:LLMClient
    ):
        self.client=client
        
    def chat(
        self,
        messages:list[dict],
        tools:list[dict]|None=None,
        temperature:float=0.7
    )->LLMResponse:
        
        return self.client.chat(
            messages=messages,
            tools=tools,
            temperature=temperature
        )

api_key=LLM_CONFIG["api_key"]
model=LLM_CONFIG["model"]
base_url=LLM_CONFIG["base_url"]
llm_client=LLMClient(model=model,api_key=api_key,base_url=base_url)
llm_service=LLMService(client=llm_client)