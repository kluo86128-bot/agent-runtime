from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.tasks import router as task_router
from app.api.tools import router as tools_router
from app.db.session import init_db
app=FastAPI(
    title="Agent Starter",
    description="A minimal AI Agent backend project",
    version="0.1.0"
)

init_db()

app.include_router(health_router)
app.include_router(task_router)
app.include_router(tools_router)