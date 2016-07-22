from django.db import models


class DataSet(models.Model):

    data = models.CharField(
        "JSON with Array of dicts with numbers",
        max_length=2048
    )

    def __str__(self):
        return '{id}'.format(id=self.id)


class TestRun(models.Model):

    NEW = 'NEW'
    INPROGRESS = 'INPROGRESS'
    DONE = 'DONE'
    STATUS_CHOICES = (
        (NEW, NEW),
        (INPROGRESS, INPROGRESS),
        (DONE, DONE)
    )

    status = models.CharField(
        max_length=2048,
        choices=STATUS_CHOICES,
        default=NEW,
        db_index=True
    )

    dataset = models.ForeignKey(
        'DataSet',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(auto_now_add=True, db_index=True)


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

    error = models.BooleanField(default=False, db_index=True)

    exception = models.TextField('Error Description', null=True)

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '{o.dataset} {o.a} {o.b} {o.result}'.format(o=self)
