from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('post_hackathon', views.post_hackathon, name='post_hackathon'),
    path('get_hackathons', views.get_hackathons, name='get_hackathons'),
    path('register_for_hackathon', views.register_for_hackathon, name='register_for_hackathon'),
    path('delete_hackathon', views.delete_hackathon, name='delete_hackathon'),
    path('submissions/', include('submissions.urls')),
]
