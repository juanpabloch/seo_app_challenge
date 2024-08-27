from django.urls import path
from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name='results'),
    path('check_task_status/', views.check_task_status, name='check_task_status'),
]