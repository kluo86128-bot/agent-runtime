from datetime import datetime
from sqlalchemy import Column,DateTime,Integer,String,Text
from app.db.session import Base

class TaskORM(Base):
    __tablename__="tasks"
    id=Column(String,primary_key=True,index=True)
    instruction=Column(Text,nullable=False)
    status=Column(String,nullable=False)
    result=Column(Text,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    
    
class TraceORM(Base):
    __tablename__="traces"
    
    id=Column(String,primary_key=True,index=True)
    task_id=Column(String,index=True,nullable=True)
    step_index=Column(Integer,nullable=False)
    action=Column(String,nullable=False)
    input=Column(Text,nullable=False)
    output=Column(Text,nullable=False)
    error_type=Column(String,nullable=True)
    error_message=Column(String,nullable=True)
    error_trace=Column(String,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow)