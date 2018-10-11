from django.conf.urls import url

from . import views
app_name = 'triumph_app'
urlpatterns = [
    url(r'^(?P<theme_id>[0-9]+)/(?P<level>[0-9]+)/$', views.challenge_view, name='challenge'),
    url(r'^$', views.index, name='index'),
]
