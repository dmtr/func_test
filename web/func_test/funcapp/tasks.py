from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=0)
def test_func(self):
    logger.info('run test_func')
    return True
