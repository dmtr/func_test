import json

from celery import chord
from celery import shared_task
from celery.result import allow_join_result
from celery.utils.log import get_task_logger

from django.db import transaction

from funcapp.models import TestSuite
from funcapp.models import TestRun
from funcapp.models import Result
from funcapp.models import ERROR
from funcapp.models import NEW
from funcapp.models import INPROGRESS
from funcapp.models import DONE

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=0)
def start_calculation(self, test_suite_id):
    logger.info('Runing test_suite %s', test_suite_id)
    with transaction.atomic():
        TestSuite.objects.filter(pk=test_suite_id).update(status=INPROGRESS)
        tests = TestRun.objects.select_related('dataset').filter(testsuite=test_suite_id, status=NEW)
        chord(test_func.subtask((d,), link_error=log_error.s(t.id)) for t in tests for d in json.loads(t.dataset.data))(update_db.s([t.id for t in tests]))
        tests.update(status=INPROGRESS)


@shared_task(bind=True, max_retries=0)
def log_error(self, task_id, testrun_id):
    logger.info('TestRun failed %s', testrun_id)
    with allow_join_result():
        result = self.AsyncResult(task_id)
        result.get(propagate=False)
        test_run = TestRun.objects.select_related('testsuite').get(pk=testrun_id)
        test_run.status = ERROR
        test_run.exception = result.traceback
        test_run.testsuite.status = ERROR
        test_run.save()
        test_run.testsuite.save()


@shared_task(bind=True, max_retries=0)
def update_db(self, results, tests):
    logger.debug('tests %s, results %s', tests, results)
    with transaction.atomic():
        ds = [(t, d) for t in TestRun.objects.select_related('dataset').filter(pk__in=tests) for d in json.loads(t.dataset.data)]
        for i, td in enumerate(ds):
            t, d = td
            Result.objects.create(
                a=d['a'],
                b=d['b'],
                result=results[i],
                testrun=t
            )
        TestSuite.objects.filter(pk=t.testsuite.id).update(status=DONE)
        TestRun.objects.filter(pk__in=tests).update(status=DONE)


@shared_task(bind=True, max_retries=0)
def test_func(self, data):
    logger.info('Runing test_func with data %s', data)
    return {'result': data['a'] + data['b']}
