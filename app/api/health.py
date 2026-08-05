from fastapi import APIRouter
from app.db.redis_client import check_redis_connection
router=APIRouter()

@router.get("/health")
def redis_health():
    return{
        "status":"ok",
        "services":{
            "api":"up",
            "redis":"up" if check_redis_connection() else "down",
        }
    }