from django.urls import path
from base import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name='results'),
    path('history/', views.history, name='history'),
    path('check_task_status/', views.check_task_status, name='check_task_status'),
    path('delete_history_item/<int:item_id>', views.delete_history_item, name='delete_history_item'),
]