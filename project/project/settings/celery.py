BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'
CELERY_TASK_RESULT_EXPIRES = 7 * 86400  # 7 days
CELERY_SEND_EVENTS = True
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_TIMEZONE = 'UTC'
import djcelery

djcelery.setup_loader()
