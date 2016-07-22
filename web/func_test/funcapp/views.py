import logging
import json

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from funcapp.forms import DataSetForm
from funcapp.forms import StartCalculationForm
from funcapp.models import DataSet
from funcapp.models import TestSuite
from funcapp.models import TestRun

logger = logging.getLogger(__name__)


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
                data=json.loads(d)
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

            messages.info(request, 'Расчет запущен')
    else:
        form = StartCalculationForm()

    return render(request, 'funcapp/calc.html', {'form': form})
