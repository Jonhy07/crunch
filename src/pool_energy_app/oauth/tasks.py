from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from datetime import datetime, timedelta



logger = get_task_logger(__name__)


SOCIAL_APPLICATION_FACEBOOK = 1
SOCIAL_APPLICATION_ADWORDS = 2

