from django.urls import path
from .views import event_list,event_detail,event_register

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:pk>/', event_detail, name='event_detail'),
    path('event/<int:pk>/register/', event_register, name='event_register'),
]