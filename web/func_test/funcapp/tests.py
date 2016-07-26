import json
from django.test import override_settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from funcapp.models import DataSet
from funcapp.models import Result
from funcapp.models import TestSuite
from funcapp.models import TestRun
from funcapp.tasks import start_calculation


class AddDataSetTest(TestCase):

    def test_ok(self):
        url = reverse('funcapp:adddataset')
        d = [{"a": 1, "b": 2}]
        j = json.dumps(d)
        response = self.client.post(url, {'dataset': j})
        self.assertEqual(response.status_code, 200)
        ds = DataSet.objects.all()
        self.assertEqual(1, len(ds))
        self.assertEqual(d, json.loads(ds[0].data))

    def test_bad_json(self):
        url = reverse('funcapp:adddataset')
        response = self.client.post(url, {'dataset': "[{'a': 1}]"})
        self.assertEqual(response.status_code, 200)
        ds = DataSet.objects.all()
        self.assertEqual(0, len(ds))


class CalculationTaskTest(TestCase):

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_ok(self):
        d = [{"a": 1, "b": 2}, {"a": 2, "b": 3}]
        dataset = DataSet.objects.create(
            data=json.dumps(d)
        )
        test_suite = TestSuite.objects.create()
        test_runs = []
        for ds in DataSet.objects.all():
            test_suite.datasets.add(ds)
            tr = TestRun.objects.create(testsuite=test_suite, dataset=ds)
            test_runs.append(tr)
        start_calculation(test_suite.id)

        test_suite.refresh_from_db()
        self.assertEqual('DONE', test_suite.status)
        self.assertEqual([dataset], [d for d in test_suite.datasets.all()])
        self.assertEqual(1, len(test_runs))
        t = test_runs[0]
        t.refresh_from_db()
        self.assertEqual('DONE', t.status)
        res = Result.objects.filter(testrun=t)
        self.assertEqual(3, json.loads(res[0].result)['result'])
