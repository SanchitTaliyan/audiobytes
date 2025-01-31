from celery import Celery # type: ignore
from celery.schedules import crontab # type: ignore
from kombu import Exchange, Queue # type: ignore

from config import cfg

celery_app = Celery(
    'proj',
    broker=f"amqp://{cfg.RABBITMQ_USERNAME}:{cfg.RABBITMQ_PASSWORD}@{cfg.RABBITMQ_HOST}:{cfg.RABBITMQ_PORT}//",
    backend=f"redis://{cfg.REDIS_HOST}:{cfg.REDIS_PORT}/{cfg.REDIS_DATABASE}",
    include=['proj.tasks']
)

# Define the task queues
celery_app.conf.task_queues = (
    Queue('default', Exchange('default', type='topic', durable=True), routing_key='default.#', durable=True),
)

# Define the default routing key
celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_default_exchange = 'default'
celery_app.conf.task_default_routing_key = 'default'
celery_app.conf.task_default_exchange_type = 'topic'
celery_app.conf.task_default_durable = True

celery_beats = {
    'print-at-8AM': {
        'task': 'proj.tasks.create_morning_episode',
        'schedule': crontab(minute=0, hour=8),  # Runs at 8 AM and 6 PM IST daily
    },
    'print-at-6PM': {
        'task': 'proj.tasks.create_eod_episode',
        'schedule': crontab(minute=0, hour=18),  # Runs at 8 AM and 6 PM IST daily
    },
    'print-at-12PM-Tuesday': {
        'task': 'proj.tasks.create_weekly_episode',
        'schedule': crontab(minute=0, hour=12, day_of_week='2'),  # Runs at 12 PM only on Tuesdays
    },
}

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires = 3600,
    worker_heartbeat=120,
    beat_schedule=celery_beats,
    timezone='Asia/Kolkata',
    broker_transport_options={
        'visibility_timeout': 6 * 60 * 60, # assuming max 2 hours to process any task
        "socket_keepalive": True,
    },
    task_acks_late=True,  # Tasks are acknowledged only when fully processed
    worker_prefetch_multiplier=1,  # reserve one task at a time
)

if __name__ == '__main__':
    celery_app.start()