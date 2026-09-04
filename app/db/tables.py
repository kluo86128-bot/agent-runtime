from datetime import datetime
from sqlalchemy import Column,DateTime,Integer,String,Text,JSON
from app.db.session import Base

class TaskORM(Base):
    __tablename__="tasks"
    id=Column(String,primary_key=True,index=True)
    instruction=Column(Text,nullable=False)
    state=Column(String,nullable=False)
    result=Column(Text,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    
    
class TraceORM(Base):
    __tablename__="traces"
    
    id=Column(String,primary_key=True,index=True)
    task_id=Column(String,index=True,nullable=True)
    model_step=Column(Integer,nullable=True)
    llm_request=Column(JSON,nullable=True)
    llm_response=Column(String,nullable=True)
    tool_call=Column(JSON,nullable=True)
    tool_result=Column(JSON,nullable=True)
    final_answer=Column(String,nullable=True)
    error_trace=Column(String,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)