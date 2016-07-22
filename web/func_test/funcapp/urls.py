from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^adddataset/$', views.add_dataset, name='adddataset'),
]
