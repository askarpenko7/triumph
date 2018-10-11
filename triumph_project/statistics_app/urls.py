from django.conf.urls import url

from . import views

app_name = 'statistics_app'
urlpatterns = [
    url(r'^$', views.empty_statistics, name='empty_statistic'),
    url(r'^(?P<group_id>([0-9]+|g_all))/(?P<student_id>([0-9]+|s_all))/(?P<date_start>(\d{2}-\d{2}-\d{4}|m_ago))/(?P<date_end>(\d{2}-\d{2}-\d{4})|today)/$', views.statistics, name='statistic'),
    url(r'^get_users_by_group/(?P<group_id>([0-9]+|g_all))/$', views.get_filters_data, name='filters_data'),
    url(r'^start_statistic$', views.start_statistic, name='start_statistic'),
    url(r'^update_statistic_time$', views.update_statistic_time, name='update_statistic_time'),
    url(r'^add_answer$', views.add_answer, name='add_answer'),
]