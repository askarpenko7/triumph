from django.conf.urls import url
from . import views

app_name = 'loginsys_app'
urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
]