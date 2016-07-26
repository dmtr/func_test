import logging

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from funcapp.forms import DataSetForm
from funcapp.forms import StartCalculationForm
from funcapp.models import DataSet
from funcapp.models import TestSuite
from funcapp.models import TestRun
from funcapp.models import Result
from funcapp.models import DONE, ERROR
from funcapp.tasks import start_calculation

logger = logging.getLogger(__name__)

NO_ERR_MSG = 'Без ошибок'
ERR_MSG = 'С ошибками'


@require_http_methods(['GET'])
def index(request):
    return render(request, 'funcapp/index.html')


@require_http_methods(['GET', 'POST'])
def add_dataset(request):
    if request.method == 'POST':
        form = DataSetForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data['dataset']
            DataSet.objects.create(
                data=d
            )
            messages.info(request, 'Данные добавлены')
    else:
        form = DataSetForm()

    return render(request, 'funcapp/adddataset.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def calculate_all(request):
    if request.method == 'POST':
        form = StartCalculationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                test_suite = TestSuite.objects.create()
                for ds in DataSet.objects.all():
                    test_suite.datasets.add(ds)
                    TestRun.objects.create(testsuite=test_suite, dataset=ds)

            start_calculation.s(test_suite.id).apply_async()
            messages.info(request, 'Расчет запущен')
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        form = StartCalculationForm()

    return render(request, 'funcapp/calc.html', {'form': form})


@require_http_methods(['GET'])
def status(request):
    ts = TestSuite.objects.filter(status__in=[DONE, ERROR]).order_by('-created')[0]
    logger.debug('Last TestSuite %s', ts)
    status = NO_ERR_MSG if ts.status == DONE else ERR_MSG
    return render(request, 'funcapp/status.html', {'status': status})


@require_http_methods(['GET'])
def results(request):
    ts = TestSuite.objects.filter(status__in=[DONE, ERROR]).order_by('-created')[0]
    logger.debug('Last TestSuite %s', ts)
    results = Result.objects.filter(testrun__testsuite=ts).select_related('testrun')
    return render(request, 'funcapp/results.html', {'results': results})


@require_http_methods(['GET'])
def errors(request):
    errors = TestRun.objects.filter(status=ERROR).select_related('dataset')
    return render(request, 'funcapp/errors.html', {'errors': errors})
