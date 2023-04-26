from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('get_all_submissions', views.get_all_submissions, name='get_all_submissions'),
    path('make_submission', views.make_submission, name='make_submission'),
    path('delete_submission', views.delete_submission, name='delete_submission'),
]
