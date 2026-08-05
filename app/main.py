from fastapi import FastAPI
from app.api.agent_trace_api import router as agent_trace_router
from app.api.task_manage_api import router as task_manage_router
from app.api.task_state_api import router as task_state_router
from app.db.session import init_db
app=FastAPI(
    title="Agent Restruct",
    description="A minimal AI Agent backend project by restructing Agent Start",
    version="0.1.0"
)

init_db()

app.include_router(agent_trace_router)
app.include_router(task_manage_router)
app.include_router(task_state_router)