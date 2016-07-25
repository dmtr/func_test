from django.db import models

NEW = 'NEW'
INPROGRESS = 'INPROGRESS'
DONE = 'DONE'
ERROR = 'ERROR'
STATUS_CHOICES = (
    (NEW, NEW),
    (INPROGRESS, INPROGRESS),
    (DONE, DONE),
    (ERROR, ERROR)
)


class DataSet(models.Model):

    data = models.CharField(
        "JSON with Array of dicts with numbers",
        max_length=2048
    )

    def __str__(self):
        return '{id}'.format(id=self.id)


class TestSuite(models.Model):

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=NEW,
        db_index=True
    )

    datasets = models.ManyToManyField(DataSet)

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '{o.id} {o.datasets}'.format(o=self)


class TestRun(models.Model):

    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=NEW,
        db_index=True
    )

    testsuite = models.ForeignKey(
        'TestSuite',
        on_delete=models.CASCADE
    )

    dataset = models.ForeignKey(
        'DataSet',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    exception = models.TextField('Error Description', null=True)

    def __str__(self):
        return '{o.id} {o.testsuite} {o.dataset}'.format(o=self)


class Result(models.Model):

    testrun = models.ForeignKey(
        'TestRun',
        on_delete=models.CASCADE
    )

    a = models.IntegerField('Number a')

    b = models.IntegerField('Number b')

    result = models.CharField(
        'Result (JSON)',
        max_length=20
        )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{o.dataset} {o.a} {o.b} {o.result}'.format(o=self)
