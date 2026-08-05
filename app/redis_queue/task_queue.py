from rq import Queue

from app.redis_base.redis_client import redis_client

task_queue=Queue(
    name="agent-tasks",
    connection=redis_client,
    default_timeout=600
)