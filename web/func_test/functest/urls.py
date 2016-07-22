from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^funcapp/', include('funcapp.urls', namespace='funcapp')),
    url(r'^$', RedirectView.as_view(url='funcapp/', permanent=False))
]
