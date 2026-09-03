# app/config/config.py
from dotenv import load_dotenv
import os


load_dotenv()

def get_required_env(name:str)->str:
    value=os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable:{name}"
        )
    return value
LLM_CONFIG={

    "api_key":get_required_env("DEEPSEEK_API_KEY"),

    "base_url":os.getenv("DEEPSEEK_BASE_URL","https://api.deepseek.com"),

    "model":os.getenv("DEEPSEEK_MODEL","deepseek-v4-flash")

}