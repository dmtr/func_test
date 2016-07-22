import logging
import json

from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from funcapp.forms import DataSetForm
from funcapp.models import DataSet

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
