from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^adddataset/$', views.add_dataset, name='adddataset'),
    url(r'^calculateall/$', views.calculate_all, name='calculateall'),
    url(r'^status/$', views.status, name='status'),
    url(r'^results/$', views.results, name='results'),
    url(r'^errors/$', views.errors, name='errors'),
]
