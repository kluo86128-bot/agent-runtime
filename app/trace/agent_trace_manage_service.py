from uuid import uuid4
from typing import Any
from app.trace.trace_schema import TraceRecord
from app.db.tables import TraceORM
from app.db.session import SessionLocal
import json
from datetime import datetime
import traceback
from app.tools.schema import ToolResultSchema
class AgentTraceManageService:
    def __init__(self):
        self._traces:dict[str,list[TraceRecord]]={}
        
    def add_trace(
        self,
        task_id:str|None=None,
        model_step:int|None=None,
        llm_request:dict[str,Any]|None=None,
        llm_response:str|None=None,
        tool_call:dict[str,Any]|None=None,
        tool_result:ToolResultSchema|None=None,
        final_answer:Any|None=None,
        error_trace:str|None=None
        )->TraceRecord:
        
        
        trace_id=str(uuid4())
        with SessionLocal() as db:
            try:
                trace_orm=TraceORM(
                    id=trace_id,
                    task_id=task_id,
                    model_step=model_step,
                    llm_request=llm_request,
                    llm_response=llm_response,
                    tool_call=tool_call,
                    tool_result=tool_result,
                    final_answer=final_answer,
                    error_trace=error_trace,
                    created_at=datetime.utcnow()
                )
                db.add(trace_orm)
                db.commit()
                db.refresh(trace_orm)
                return self._to_record(trace_orm)
            except Exception as e:
                db.rollback()
                raise

        
    def get_trace(self,task_id)->list[TraceRecord]:
        with SessionLocal() as db:
            try:
                trace_orms=db.query(TraceORM).filter(TraceORM.task_id==task_id).order_by(TraceORM.model_step.asc()).all()
                return [self._to_record(trace_orm) for trace_orm in trace_orms]
            except:
                db.close()
                raise RuntimeError(f"\nerror in get_trace of {task_id}:{traceback.format_exc()}")
                
    
    
    def _to_record(self,trace_orm:TraceORM)->TraceRecord:

        return TraceRecord(
            trace_id=trace_orm.id,
            task_id=trace_orm.task_id,
            model_step=trace_orm.model_step,
            llm_request=trace_orm.llm_request,
            llm_response=trace_orm.llm_response,
            tool_call=trace_orm.tool_call,
            tool_result=trace_orm.tool_result,
            final_answer=trace_orm.final_answer,
            error_trace=trace_orm.error_trace,
            created_at=trace_orm.created_at
        )
agent_trace_manage_service=AgentTraceManageService()
