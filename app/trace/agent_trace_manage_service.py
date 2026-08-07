from uuid import uuid4
from typing import Any
from app.trace.trace_schema import TraceRecord
from app.db.tables import TraceORM
from app.db.session import SessionLocal
import json
from datetime import datetime
import traceback
class AgentTraceManageService:
    def __init__(self):
        self._traces:dict[str,list[TraceRecord]]={}
        
    def add_trace(
        self,
        task_id:str,
        step_index:int,
        action:str,
        input:Any=None,
        output:Any=None,
        error_type:str|None=None,
        error_message:str|None=None,
        error_trace:str|None=None
        )->TraceRecord:
        
        
        trace_id=str(uuid4())
        input_text=json.dumps(input,ensure_ascii=False) if input is not None else None
        output_text=json.dumps(output,ensure_ascii=False) if input is not None else None
        with SessionLocal() as db:
            try:
                trace_orm=TraceORM(
                    id=trace_id,
                    task_id=task_id,
                    step_index=step_index,
                    action=action,
                    input=input_text,
                    output=output_text,
                    error_type=error_type,
                    error_message=error_message,
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
                trace_orms=db.query(TraceORM).filter(TraceORM.task_id==task_id).order_by(TraceORM.step_index.asc()).all()
                return [self._to_record(trace_orm) for trace_orm in trace_orms]
            except:
                db.close()
                
                return [TraceRecord(
                trace_id="None",
                task_id=task_id,
                step_index=0,
                action="None",
                input="None",
                output="None",
                error_type="None",
                error_message="None",
                error_trace="None",
                created_at=datetime.utcnow()
            )]
    
    def _to_record(self,trace_orm:TraceORM)->TraceRecord:
        input_value=json.loads(trace_orm.input) if trace_orm.input else None
        output_value=json.loads(trace_orm.output) if trace_orm.output else None
        
        return TraceRecord(
            trace_id=trace_orm.id,
            task_id=trace_orm.task_id,
            step_index=trace_orm.step_index,
            action=trace_orm.action,
            input=input_value,
            output=output_value,
            error_type=trace_orm.error_type,
            error_message=trace_orm.error_message,
            error_trace=trace_orm.error_trace,
            created_at=trace_orm.created_at
        )
agent_trace_manage_service=AgentTraceManageService()
