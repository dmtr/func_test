import json

from celery import chord
from celery import shared_task
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
        chord(test_func.s(d) for t in tests for d in json.loads(t.dataset.data))(update_db.s([t.id for t in tests]))
        tests.update(status=INPROGRESS)


@shared_task(bind=True, max_retries=0)
def update_db(self, results, tests):
    logger.debug('tests %s, results %s', tests, results)
    failed = []
    not_failed = []
    ds = [(t, d) for t in TestRun.objects.select_related('dataset').filter(pk__in=tests) for d in json.loads(t.dataset.data)]
    for i, td in enumerate(ds):
        t, d = td
        result = results[i]
        if isinstance(result, Exception):
            failed.append((t, result))
        else:
            Result.objects.create(
                a=d['a'],
                b=d['b'],
                result=json.dumps(result),
                testrun=t
            )
            not_failed.append(t)

    TestRun.objects.filter(pk__in=[t.id for t in not_failed]).update(status=DONE)
    for f in failed:
        t, e = f
        TestRun.objects.filter(pk=t.id).update(
            status=ERROR,
            exception=repr(e)
        )

    if failed:
        TestSuite.objects.filter(pk=failed[0][0].testsuite.id).update(status=ERROR)
    else:
        TestSuite.objects.filter(pk=not_failed[0].testsuite.id).update(status=DONE)


@shared_task(bind=True, max_retries=0)
def test_func(self, data):
    logger.info('Runing test_func with data %s', data)
    return {'result': data['a'] + data['b']}
