from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.config.config import settings
from sqlalchemy import event
from app.log.logger import logger
DATABASE_URL=settings.DATABASE_URL

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

@event.listens_for(engine,"checkout")
def on_checkout(dbapi_connection,connection_record,connection_proxy):
    logger.info(
        "DB connection checkout | %s",
        engine.pool.status()
    )
    
@event.listens_for(engine,"checkin")
def on_checkin(dbapi_connection,connection_record):
    logger.info(
        "DB connection checkin | %s",
        engine.pool.status()
    )

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()

def init_db()->None:
    Base.metadata.create_all(bind=engine)
    
def get_db_session():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()